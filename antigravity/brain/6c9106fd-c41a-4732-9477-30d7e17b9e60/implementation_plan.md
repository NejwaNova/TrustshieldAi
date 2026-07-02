# Implementation Plan - Python (FastAPI) Backend Migration

Migrate the TrustShield AI digital trust platform backend from Node.js (Express) to Python (FastAPI) as requested. This migration preserves the existing database JSON schema, the multi-shield threat analysis engine, standard SSE streaming, webhook triggers, and the high-fidelity glassmorphic HTML/CSS/JS frontend dashboard.

## Proposed Changes

### Configuration & Utilities

#### [NEW] [requirements.txt](file:///C:/Users/PC/.gemini/antigravity/scratch/trustshield-ai/requirements.txt)
Define standard Python dependencies for FastAPI:
- `fastapi`
- `uvicorn`

#### [MODIFY] [run.py](file:///C:/Users/PC/.gemini/antigravity/scratch/trustshield-ai/run.py)
Update startup automation script to:
1. Verify Python 3 is installed.
2. Install Python dependencies from `requirements.txt` using `pip install`.
3. Start the FastAPI server using `python backend/server.py` or `uvicorn`.

#### [MODIFY] [package.json](file:///C:/Users/PC/.gemini/antigravity/scratch/trustshield-ai/package.json)
Update `"start"` script to trigger the Python server for seamless backward compatibility if `npm start` is invoked:
- `"start": "python backend/server.py"`

---

### Backend Logic & API Layer

#### [NEW] [database.py](file:///C:/Users/PC/.gemini/antigravity/scratch/trustshield-ai/backend/database.py)
Replicate Node.js database helper class (`SimpleDB`) in Python:
- Load/Save to `backend/db_store.json` using Python `json` library.
- Implement `get_scans()`, `add_scan(scan_data)`, `get_stats()`, `get_integrations()`, and `update_integration(...)`.
- Thread-safe operations using file locks or simple Python structure updates.

#### [NEW] [engine.py](file:///C:/Users/PC/.gemini/antigravity/scratch/trustshield-ai/backend/engine.py)
Replicate the multi-shield composite scoring math and threat identification heuristics in Python:
- Implement `TrustShieldEngine.analyze(...)`.
- Include matching heuristics for Email, Website, Deepfake, Prompt, QR, and Document shields.
- Compile natural language markdown reports and math LaTeX details.

#### [NEW] [server.py](file:///C:/Users/PC/.gemini/antigravity/scratch/trustshield-ai/backend/server.py)
FastAPI REST API server matching current Node routes:
- `GET /api/scans` -> Return historical scans.
- `POST /api/scan` -> Scan payload and broadcast result.
- `GET /api/stats` -> Get computed distribution statistics.
- `GET /api/integrations` -> Get integrations map.
- `POST /api/integrations/{platform}` -> Update platform state.
- `POST /api/integrations/webhook/{platform}` -> Process external triggers.
- `GET /api/stream` -> Server-Sent Events (SSE) using standard Starlette StreamingResponse.
- Serve static files from `/frontend` and fallback SPA route.

---

### Clean Up

#### [DELETE] [database.js](file:///C:/Users/PC/.gemini/antigravity/scratch/trustshield-ai/backend/database.js)
#### [DELETE] [engine.js](file:///C:/Users/PC/.gemini/antigravity/scratch/trustshield-ai/backend/engine.js)
#### [DELETE] [server.js](file:///C:/Users/PC/.gemini/antigravity/scratch/trustshield-ai/backend/server.js)

---

## Verification Plan

### Automated Tests
- Run backend verification scripts to ensure FastAPI serves matching JSON shapes to the frontend.

### Manual Verification
- Start the server using `python run.py`.
- Access the dashboard at `http://127.0.0.1:8000`.
- Verify the following dashboard workflows:
  1. Manual Scan Console (Inputting raw prompts or files, getting detailed composite score card + explanation).
  2. Ingestion/Webhook Simulator (Clicking simulated webhook cards, observing live sliding toast alerts via SSE).
  3. Integration settings (Connecting/disconnecting channels).
  4. Tabs (switching dashboard tabs and reading audit logs).
