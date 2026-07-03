import os
import json
import asyncio
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse

from backend.database import SimpleDB
from backend.engine import TrustShieldEngine

app = FastAPI(title="TrustShield AI Backend")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = SimpleDB()
engine = TrustShieldEngine()

# SSE clients queue list
sse_queues = []

def broadcast_event(event_type: str, data: dict):
    payload = json.dumps({"event": event_type, "data": data})
    for queue in sse_queues:
        try:
            queue.put_nowait(payload)
        except Exception as e:
            print(f"Error putting event to queue: {e}")

# Request schemas
class ScanRequest(BaseModel):
    item: str
    type: str
    source: Optional[str] = None
    filename: Optional[str] = None

class IntegrationRequest(BaseModel):
    connected: bool
    token: str
    webhook: Optional[str] = ""

class WebhookRequest(BaseModel):
    sender: str
    content: str
    channel: Optional[str] = None
    attachment_name: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str

class SubscriptionRequest(BaseModel):
    username: str
    plan: str

# API Endpoints
@app.post("/api/login")
async def login_operator(req: LoginRequest):
    if req.username == "admin" and req.password == "admin":
        db_users = db.load_all().get("users", [])
        user = next((u for u in db_users if u.get("username") == "admin"), None)
        if not user:
            user = {"username": "admin", "role": "Security Operator", "subscription": "Free Tier"}
        return {
            "status": "authenticated",
            "user": user
        }
    else:
        raise HTTPException(
            status_code=401,
            detail="Invalid operator credentials"
        )

@app.post("/api/subscription")
async def update_subscription(req: SubscriptionRequest):
    user = db.set_subscription(req.username, req.plan)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    broadcast_event("subscription_update", {
        "username": req.username,
        "subscription": req.plan
    })
    
    return {
        "status": "updated",
        "user": user
    }

@app.get("/api/scans")
async def get_scans():
    return db.get_scans()

@app.post("/api/scan")
async def execute_scan(req: ScanRequest):
    analysis = engine.analyze(req.item, req.type, req.filename or "")
    
    # Save scan to DB
    scan_entry = db.add_scan({
        "item": req.item,
        "type": req.type,
        "risk_score": analysis["risk_score"],
        "result": analysis["result"],
        "source": req.source or "Web Dashboard",
        "details": analysis["explanation"]
    })

    # Broadcast event
    broadcast_event("new_scan", {
        "scan": scan_entry,
        "stats": db.get_stats()
    })

    return {
        "scan": scan_entry,
        "analysis": analysis
    }

@app.get("/api/stats")
async def get_stats():
    return db.get_stats()

@app.get("/api/integrations")
async def get_integrations():
    return db.get_integrations()

@app.post("/api/integrations/{platform}")
async def update_integration(platform: str, req: IntegrationRequest):
    result = db.update_integration(platform, req.connected, req.token, req.webhook)
    if not result:
        raise HTTPException(status_code=404, detail="Platform not supported")
    return result

@app.post("/api/integrations/webhook/{platform}")
async def process_webhook(platform: str, req: WebhookRequest):
    integrations = db.get_integrations()
    if platform not in integrations:
        raise HTTPException(status_code=404, detail="Integration not found")

    if not integrations[platform].get("connected", False):
        raise HTTPException(
            status_code=400, 
            detail=f"{platform.capitalize()} integration is not connected/enabled"
        )

    platform_cap = platform.capitalize()
    source_channel = f"{platform_cap} ({req.channel})" if req.channel else f"{platform_cap} Direct"

    # Detect asset type based on contents & attachment
    item_content = req.content
    asset_type = "Text"
    filename = ""

    if req.attachment_name:
        filename = req.attachment_name
        ext = filename.split(".")[-1].lower() if "." in filename else ""
        if ext in ["mp4", "mov", "avi"]:
            asset_type = "Video"
        elif ext in ["mp3", "wav", "aac"]:
            asset_type = "Audio"
        elif ext in ["png", "jpg", "jpeg"]:
            asset_type = "Image"
        elif ext in ["pdf", "docx", "xlsx", "zip"]:
            asset_type = "Document"
    elif "http://" in item_content or "https://" in item_content:
        asset_type = "URL"
    elif "ignore previous" in item_content.lower() or "dan" in item_content.lower():
        asset_type = "Text / Prompt"
    elif platform == "gmail":
        asset_type = "Email"

    # Analyze content
    analysis = engine.analyze(item_content, asset_type, filename)

    # Save to database (truncate items > 80 chars for simple overview rendering)
    db_item_text = item_content if len(item_content) < 80 else item_content[:77] + "..."
    scan_entry = db.add_scan({
        "item": db_item_text,
        "type": asset_type,
        "risk_score": analysis["risk_score"],
        "result": analysis["result"],
        "source": f"Webhook: {source_channel}",
        "details": analysis["explanation"]
    })

    # Broadcast event
    broadcast_event("webhook_alert", {
        "platform": platform,
        "sender": req.sender,
        "scan": scan_entry,
        "stats": db.get_stats()
    })

    return {
        "status": "processed",
        "verdict": analysis["verdict"],
        "score": analysis["risk_score"],
        "details": analysis["details"]
    }

# SSE Streaming
@app.get("/api/stream")
async def sse_endpoint(request: Request):
    async def event_generator():
        queue = asyncio.Queue()
        sse_queues.append(queue)
        try:
            while True:
                if await request.is_disconnected():
                    break
                try:
                    # Wait for message with a timeout of 10s for heartbeats
                    data = await asyncio.wait_for(queue.get(), timeout=10.0)
                    yield f"data: {data}\n\n"
                except asyncio.TimeoutError:
                    yield ": ping\n\n"
        finally:
            if queue in sse_queues:
                sse_queues.remove(queue)

    return StreamingResponse(event_generator(), media_type="text/event-stream")

# Frontend static files routing
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))

@app.get("/")
async def get_index():
    return FileResponse(os.path.join(frontend_dir, "index.html"))

@app.get("/{file_name}")
async def get_static_file(file_name: str):
    file_path = os.path.join(frontend_dir, file_name)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)
    # Default fallback to index.html for SPA URLs
    return FileResponse(os.path.join(frontend_dir, "index.html"))

@app.get("/{path:path}")
async def catch_all(path: str):
    return FileResponse(os.path.join(frontend_dir, "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.server:app", host="127.0.0.1", port=8000, reload=True)
