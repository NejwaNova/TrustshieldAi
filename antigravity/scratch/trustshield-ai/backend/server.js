import express from 'express';
import cors from 'cors';
import path from 'path';
import { fileURLToPath } from 'url';
import { SimpleDB } from './database.js';
import { TrustShieldEngine } from './engine.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const port = process.env.PORT || 8000;

// Enable CORS and JSON parsing
app.use(cors());
app.use(express.json());

const db = new SimpleDB();
const engine = new TrustShieldEngine();

// SSE clients list
const sseClients = [];

// Helper function to broadcast events to all active SSE clients
function broadcastEvent(eventType, data) {
    const payload = JSON.stringify({ event: eventType, data: data });
    for (const clientRes of sseClients) {
        try {
            clientRes.write(`data: ${payload}\n\n`);
        } catch (err) {
            console.error("Error writing to SSE client:", err);
        }
    }
}

// Keep-alive heartbeat (ping) for SSE clients every 10 seconds
setInterval(() => {
    for (const clientRes of sseClients) {
        try {
            clientRes.write(`: ping\n\n`);
        } catch (err) {
            // Error handled during close or next write
        }
    }
}, 10000);

// API Endpoints
app.get('/api/scans', (req, res) => {
    res.json(db.getScans());
});

app.post('/api/scan', (req, res) => {
    const { item, type, source, filename } = req.body;
    
    if (item === undefined || type === undefined) {
        return res.status(400).json({ detail: "item and type are required parameters" });
    }

    const analysis = engine.analyze(item, type, filename);

    // Save scan to database
    const scanEntry = db.addScan({
        item: item,
        type: type,
        risk_score: analysis.risk_score,
        result: analysis.result,
        source: source || "Web Dashboard",
        details: analysis.explanation
    });

    // Broadcast update to dashboard in real-time
    broadcastEvent("new_scan", {
        scan: scanEntry,
        stats: db.getStats()
    });

    res.json({
        scan: scanEntry,
        analysis: analysis
    });
});

app.get('/api/stats', (req, res) => {
    res.json(db.getStats());
});

app.get('/api/integrations', (req, res) => {
    res.json(db.getIntegrations());
});

app.post('/api/integrations/:platform', (req, res) => {
    const { platform } = req.params;
    const { connected, token, webhook } = req.body;

    const result = db.updateIntegration(platform, connected, token, webhook);
    if (!result) {
        return res.status(404).json({ detail: "Platform not supported" });
    }

    res.json(result);
});

app.post('/api/integrations/webhook/:platform', (req, res) => {
    const { platform } = req.params;
    const { sender, content, channel, attachment_name } = req.body;

    if (sender === undefined || content === undefined) {
        return res.status(400).json({ detail: "sender and content are required parameters" });
    }

    const integrations = db.getIntegrations();
    if (!(platform in integrations)) {
        return res.status(404).json({ detail: "Integration not found" });
    }

    if (!integrations[platform].connected) {
        const platformNameCap = platform.charAt(0).toUpperCase() + platform.slice(1);
        return res.status(400).json({ detail: `${platformNameCap} integration is not connected/enabled` });
    }

    const platformCap = platform.charAt(0).toUpperCase() + platform.slice(1);
    const sourceChannel = channel ? `${platformCap} (${channel})` : `${platformCap} Direct`;

    // Detect asset type based on contents & attachment
    const itemContent = content;
    let assetType = "Text";
    let filename = "";

    if (attachment_name) {
        filename = attachment_name;
        const ext = filename.split(".").pop().toLowerCase();
        if (["mp4", "mov", "avi"].includes(ext)) {
            assetType = "Video";
        } else if (["mp3", "wav", "aac"].includes(ext)) {
            assetType = "Audio";
        } else if (["png", "jpg", "jpeg"].includes(ext)) {
            assetType = "Image";
        } else if (["pdf", "docx", "xlsx", "zip"].includes(ext)) {
            assetType = "Document";
        }
    } else if (itemContent.includes("http://") || itemContent.includes("https://")) {
        assetType = "URL";
    } else if (itemContent.toLowerCase().includes("ignore previous") || itemContent.toLowerCase().includes("dan")) {
        assetType = "Text / Prompt";
    } else if (platform === "gmail") {
        assetType = "Email";
    }

    // Analyze content
    const analysis = engine.analyze(itemContent, assetType, filename);

    // Save scan to database (cut down items > 80 chars for simple overview rendering)
    const dbItemText = itemContent.length < 80 ? itemContent : itemContent.slice(0, 77) + "...";
    const scanEntry = db.addScan({
        item: dbItemText,
        type: assetType,
        risk_score: analysis.risk_score,
        result: analysis.result,
        source: sourceChannel,
        details: analysis.explanation
    });

    // Broadcast event to frontend SSE
    broadcastEvent("webhook_alert", {
        platform: platform,
        sender: sender,
        scan: scanEntry,
        stats: db.getStats()
    });

    res.json({
        status: "processed",
        verdict: analysis.verdict,
        score: analysis.risk_score,
        details: analysis.details
    });
});

// SSE endpoint
app.get('/api/stream', (req, res) => {
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');
    res.flushHeaders();

    sseClients.push(res);

    req.on('close', () => {
        const index = sseClients.indexOf(res);
        if (index !== -1) {
            sseClients.splice(index, 1);
        }
    });
});

// Serve frontend static assets
const frontendDir = path.resolve(path.join(__dirname, '..', 'frontend'));
app.use(express.static(frontendDir));

// Fallback to index.html for SPA routes
app.get('*', (req, res) => {
    res.sendFile(path.join(frontendDir, 'index.html'));
});

// Start the server
app.listen(port, () => {
    console.log(`TrustShield AI Server running at http://127.0.0.1:${port}`);
});
