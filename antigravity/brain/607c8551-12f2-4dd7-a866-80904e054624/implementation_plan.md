# Implementation Plan - Port Backend from Python to Node.js

This plan outlines the steps to replace the Python/FastAPI backend of TrustShield AI with a Node.js/Express backend while maintaining the same APIs, features, and UI compatibility.

## User Review Required

> [!IMPORTANT]
> The backend transition will replace the Python server. We will delete the Python backend files (`main.py`, `database.py`, `engine.py`, `__init__.py`) and replace them with their Node.js equivalents (`server.js`, `database.js`, `engine.js`). We will also update the root startup scripts.

## Proposed Changes

We will introduce a `package.json` in the root of the project to manage Node.js dependencies (`express`, `cors`) and run scripts. We will implement the backend using ES Modules (`import`/`export`) by setting `"type": "module"` in `package.json`.

---

### Root Configuration & Setup

#### [NEW] [package.json](file:///C:/Users/PC/.gemini/antigravity/scratch/trustshield-ai/package.json)
- Define metadata for the project.
- Specify dependency libraries: `express` and `cors`.
- Add script `"start": "node backend/server.js"`.

#### [MODIFY] [run.py](file:///C:/Users/PC/.gemini/antigravity/scratch/trustshield-ai/run.py)
- Modify `run.py` to check for `node` and `npm`, run `npm install` to set up Node.js dependencies, and then execute `npm start` (or `node backend/server.js`) to launch the application. This ensures users running the old `python run.py` startup script will still get a working server.

#### [MODIFY] [README.md](file:///C:/Users/PC/.gemini/antigravity/scratch/trustshield-ai/README.md)
- Update the backend technical details section.
- Change the quick-start instructions to include Node.js instructions (`npm install && npm start`).

---

### Backend Component (Node.js)

#### [NEW] [database.js](file:///C:/Users/PC/.gemini/antigravity/scratch/trustshield-ai/backend/database.js)
- Re-implement `SimpleDB` from [database.py](file:///C:/Users/PC/.gemini/antigravity/scratch/trustshield-ai/backend/database.py).
- Handle reading and writing `db_store.json` using Node.js `fs` module.
- Maintain the same default seed data structure.
- Re-implement functions `getScans()`, `addScan(scanData)`, `getStats()`, `getIntegrations()`, and `updateIntegration(name, connected, token, webhook)`.

#### [NEW] [engine.js](file:///C:/Users/PC/.gemini/antigravity/scratch/trustshield-ai/backend/engine.js)
- Re-implement the `TrustShieldEngine` from [engine.py](file:///C:/Users/PC/.gemini/antigravity/scratch/trustshield-ai/backend/engine.py).
- Re-implement the composite threat score formula using JavaScript math functions:
  \[ S_{\text{composite}} = \max(S_{\text{critical}}) \times 0.6 + \left( \frac{\sum (W_i \times S_i)}{\sum W_i} \right) \times 0.4 \]
- Re-implement rules for Email Shield, Website Shield, Deepfake Shield, Prompt Shield, QR Shield, and Document Shield.
- Maintain the identical formatting structure for natural language explanations (markdown format with LaTeX math equations block).

#### [NEW] [server.js](file:///C:/Users/PC/.gemini/antigravity/scratch/trustshield-ai/backend/server.js)
- Build an Express server replacing [main.py](file:///C:/Users/PC/.gemini/antigravity/scratch/trustshield-ai/backend/main.py).
- Mount the public frontend static folder to `/`.
- Implement API routing for:
  - `GET /api/scans`
  - `POST /api/scan`
  - `GET /api/stats`
  - `GET /api/integrations`
  - `POST /api/integrations/:platform`
  - `POST /api/integrations/webhook/:platform`
  - `GET /api/stream` (SSE Event Source endpoint with heartbeat keep-alive)
- Support broadcasting scan/webhook alerts to all active SSE client connections.

#### [DELETE] [main.py](file:///C:/Users/PC/.gemini/antigravity/scratch/trustshield-ai/backend/main.py)
#### [DELETE] [database.py](file:///C:/Users/PC/.gemini/antigravity/scratch/trustshield-ai/backend/database.py)
#### [DELETE] [engine.py](file:///C:/Users/PC/.gemini/antigravity/scratch/trustshield-ai/backend/engine.py)
#### [DELETE] [__init__.py](file:///C:/Users/PC/.gemini/antigravity/scratch/trustshield-ai/backend/__init__.py)

---

## Verification Plan

### Automated Tests
- Since there are no existing automated tests, we will verify manually by starting the Node.js server and testing client compatibility.

### Manual Verification
1. Run the startup script `python run.py` (which runs `npm install` and starts the Node.js server).
2. Verify that the Express server starts on port `8000` and serves the frontend.
3. Access the web dashboard in the browser.
4. Run a simulated scan from the UI to ensure:
   - Request is processed by the new Node.js engine.
   - Composite math formula calculates matching values.
   - Scan gets saved in `db_store.json`.
   - Scan results render in the UI with correct styling and explanation.
5. Go to the Integrations tab, enable an integration, and use the Simulator in the UI to trigger a simulated webhook scan. Check that:
   - SSE connection receives `webhook_alert`.
   - Toast popup is displayed.
   - Dashboard stats updates in real-time.
