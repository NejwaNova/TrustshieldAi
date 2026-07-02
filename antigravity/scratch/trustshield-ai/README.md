# TrustShield AI - Unified Digital Trust Platform

TrustShield AI is a unified digital trust platform and deepfake defense framework designed to demux incoming digital assets and evaluate security threats in real-time across multiple Shields.

> [!IMPORTANT]
> **Active Workspace Recommendation**:
> Since you do not have a currently active workspace, we recommend opening the folder `C:\Users\PC\.gemini\antigravity\scratch\trustshield-ai` as your project's active workspace.

---

## Key Features

1. **7 Specialized Safety Shields**: Ingests payloads and parses them via Email, URL, Deepfake, Prompt, QR, and Document shields, synthesizing logs via the AI Explanation Engine.
2. **Explainable Composite Trust Scores**: Uses the exact mathematical verification formula:
   \[ S_{\text{composite}} = \max(S_{\text{critical}}) \times 0.6 + \left( \frac{\sum (W_i \times S_i)}{\sum W_i} \right) \times 0.4 \]
3. **Universal Trust Adapter**: Connect platforms (Gmail, Telegram, Slack, Discord, WhatsApp) to auto-verify active communications.
4. **Interactive Messaging Simulator**: Test webhook integrations by sending simulated social media phishing links and cloned audio attachments directly in the interface.
5. **Real-time SSE Notification Banner**: Displays warning toasts instantly when incoming threats are blocked or quarantined.

---

## Quick Start Setup

### Prerequisites
Make sure **Node.js** (v18+) is installed on your machine.

### Launching the Application
You can run the startup script to automatically install dependencies and start the server:

```powershell
python run.py
```

Alternatively, you can run the standard Node/npm commands directly from the project root:

```powershell
npm install
npm start
```

Once running, open your web browser and navigate to:
**[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## Technical Details

- **Frontend**: Single-Page App (SPA) built using HTML5, modern Glassmorphic Vanilla CSS, and JavaScript.
- **Backend**: Express (Node.js) serving REST APIs and real-time Server-Sent Events (SSE).
- **Persistence**: Relational file-based JSON DB tracking users, logs, scans, and configs.
