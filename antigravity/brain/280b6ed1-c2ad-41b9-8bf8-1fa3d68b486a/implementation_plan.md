# Implementation Plan - TrustShield AI

TrustShield AI is a Unified Digital Trust Platform and Deepfake Defense Framework. We will build a highly polished, interactive, and visually stunning web application that satisfies all criteria in the technical proposal and matches the high-fidelity UI mockup.

To meet the user requirements, we will implement:
1. **Interactive Frontend**: A single-page application (SPA) featuring a dark modern glassmorphism design with a fully functional dashboard, live statistics, scan history, interactive scan tool, and custom charts.
2. **FastAPI Backend**: A Python backend to handle ingestion, coordinate the 7 security shields, compute risk scores using the exact mathematical formula, and generate natural language threat intelligence using template-based rules (with optional Gemini API fallback).
3. **Mock Data & Real-Time Scans**: Ingest custom text/URLs and file simulations, demonstrating the Universal Trust Adapter routing payloads through the seven shields.

## Proposed Subdirectory
We will build the application in:
`C:\Users\PC\.gemini\antigravity\scratch\trustshield-ai`

We recommend the user set this subdirectory as the active workspace once created.

---

## Proposed Architecture & File Structure

```
trustshield-ai/
├── backend/
│   ├── __init__.py
│   ├── main.py            # FastAPI App, routes, static file serving
│   ├── engine.py          # Trust Score Engine & 7 Shield logic
│   └── database.py        # Relational DB mockup (using SQLite / file persistence)
├── frontend/
│   ├── index.html         # Rich HTML5 layout & UI sections
│   ├── styles.css         # Sleek modern CSS, Glassmorphism, animations
│   └── app.js             # Frontend routing, charts, user events, API integration
├── run.py                 # Easy startup script (pip installation & launch)
└── README.md              # Setup and execution guide
```

---

## Technical Specifications

### 1. The 7 Shields
- **Email Shield**: Parses headers/MIME (SPF, DKIM, DMARC validation) and runs intent analysis.
- **Website Shield**: Evaluates typosquatting, redirects, and queries reputation lists.
- **Deepfake Shield**: Detects visual artifacts (GAN/diffusion) in frames and audio phase anomalies.
- **Prompt Shield**: Screens against prompt injection vectors and jailbreaks.
- **QR Shield**: Detects, isolates, and decodes QR codes.
- **Document Shield**: Inspects active code, macros, and XML schemas.
- **AI Explanation Engine**: Synthesizes scores and yields natural language explanations.

### 2. Social Media & Integrations (Universal Trust Adapter)
To enable multi-channel threat detection, we will implement:
- **Integrations Panel**: A dedicated section to configure Discord Webhooks, Slack App Tokens, Telegram Bot Tokens, Gmail OAuth, and WhatsApp Helpline Numbers.
- **Webhook Ingestion Endpoints**: Backend API endpoints `/api/integrations/webhook/{platform}` simulating real-time payloads sent by Slack, Telegram, Discord, Gmail, and WhatsApp.
- **Visual Alert Notifications**: A real-time toast alert system that triggers when an incoming social media message is scanned and found suspicious, updating the global dashboard stats and recent scans list dynamically.
- **Social Media Simulator**: A dedicated testing interface in the frontend allowing users to trigger pre-packaged or custom threat messages from specific channels (e.g., a suspicious URL in a Discord announcement, or a deepfake voice memo forwarded on Telegram).

### 3. Trust Score Engine Math
The backend will compute the composite risk score using the exact formula:
\[ S_{\text{composite}} = \max(S_{\text{critical}}) \times 0.6 + \left( \frac{\sum (W_i \times S_i)}{\sum W_i} \right) \times 0.4 \]
We will display this equation and its active inputs in the scan result breakdown.

---

## Verification Plan

### Automated Verification
We will run:
- Python backend server validation (starting FastAPI, checking API health).
- Frontend visual audit using a browser/subagent or manual validation.

### Manual Verification
- Testing custom scans for all 4 asset classes: Email, URLs, Media files, and Prompts.
- Checking that stats increment on new scans, historical logs are stored, and the layout looks identical to the mockup.
