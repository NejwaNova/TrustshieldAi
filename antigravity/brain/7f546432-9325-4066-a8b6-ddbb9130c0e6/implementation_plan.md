# TrustShield AI Implementation Plan

This plan outlines the steps to build and refine the **TrustShield AI** platform, aligning the frontend design, visual themes, layout structure, and backend logic with the technical proposal specifications and the high-fidelity visual mockups.

## Key Goals
1. **Visual Alignment with Mockup**:
   - Style the landing hero, sidebar navigation, stats cards, recent scans table, doughnut chart, quick scan tab bar, and security tips to match the mockups.
   - Employ a premium dark-themed layout with glassmorphic panels, neon glows, and smooth transitions.
2. **Mathematical & Score Consistency**:
   - Align the classification thresholds in the backend engine with the mockup score guide (0-30: Safe, 31-60: Low Risk, 61-80: Medium Risk, 81-100: High Risk).
   - Calibrate initial database scans and stats (Total Scans: 24, Threats: 12, Safe: 12, Average Risk: 57) and doughnut chart distribution (High: 35%, Medium: 25%, Low: 20%, Safe: 20%) to match the mockup exactly.
3. **Interactive Simulation & Dynamic Updates**:
   - Enable interactive quick-scanning from the dashboard tabs.
   - Connect platform webhook simulators to trigger real-time SSE notifications and update dashboard states dynamically.

---

## Proposed Changes

### Backend Components

#### [MODIFY] [engine.py](file:///C:/Users/PC/.gemini/antigravity/scratch/trustshield-ai/backend/engine.py)
- Update score thresholds to follow the mockup-defined ranges:
  - `0 - 30`: **Safe** (Result: "Safe", Verdict: "Allowed", Action: "Allow execution; log metadata.")
  - `31 - 60`: **Low Risk** (Result: "Low Risk", Verdict: "User Warned", Action: "Warn user; enforce visual isolation.")
  - `61 - 80`: **Medium Risk** (Result: "Medium Risk", Verdict: "Asset Quarantined", Action: "Quarantine asset; prompt explicit confirmation.")
  - `81 - 100`: **High Risk** (Result: "High Risk", Verdict: "Blocked", Action: "Block payload entirely; trigger response workflows.")
- Update natural language reports to dynamically reflect these exact descriptions.
- Ensure model baseline values align logically with these thresholds (e.g., typosquat URL score baseline set to 85, CEO spoof email BEC set to 92, deepfake video set to 88, prompt injection set to 73, and AI-generated text set to 40).

#### [MODIFY] [database.py](file:///C:/Users/PC/.gemini/antigravity/scratch/trustshield-ai/backend/database.py)
- Calibrate the initial scan list to contain:
  1. CEO Spoof email scan: `92/100` (High Risk)
  2. Typosquat URL scan: `85/100` (High Risk)
  3. Deepfake video scan: `88/100` (High Risk)
  4. Jailbreak prompt scan: `73/100` (Medium Risk)
  5. AI-generated text scan: `40/100` (Low Risk)
- Adjust the initial `get_stats()` returns so that the defaults perfectly mirror the mockup:
  - `total_scans` = 24
  - `threats_detected` = 12
  - `safe_items` = 12
  - `avg_risk_score` = 57
  - `distribution` = `{"critical": 35, "high": 25, "medium": 20, "safe": 20}` (High Risk: 35%, Medium Risk: 25%, Low Risk: 20%, Safe: 20%)
- When new scans are performed, calculate stats dynamically using the calibrated base.

---

### Frontend Components

#### [MODIFY] [index.html](file:///C:/Users/PC/.gemini/antigravity/scratch/trustshield-ai/frontend/index.html)
- Redesign the sidebar layout to match the mockup exactly:
  - Links: `Dashboard` (active), `Scan` (with submenu headers for `Email / Message`, `URL / Website`, `Image / Video / Audio`, `Text / Prompt`), `History`, `Reports`, and `Settings`.
  - Sidebar footer card: "Stay Protected" with subtitle "Enable real-time protection across your devices." and a togglable shield check.
- Update the table columns in the "Recent Ingestion Telemetry" to match:
  - `Item`, `Type`, `Risk Score`, `Result`, and `Time`.
- Update the "Risk Score Guide" ranges, labels, and descriptions in the HTML.
- Update the "Security Tips" panel to match the mockup list exactly:
  - Tip 1: "Always verify unknown emails and links before clicking."
  - Tip 2: "Avoid sharing sensitive information in unsolicited messages."
- Ensure the quick scan tab box layout and "Scan Now" button have matching text and styles.

#### [MODIFY] [app.js](file:///C:/Users/PC/.gemini/antigravity/scratch/trustshield-ai/frontend/app.js)
- Update the javascript states to use the corrected risk scale:
  - High Risk: `risk_score >= 81` (Red)
  - Medium Risk: `61 <= risk_score <= 80` (Orange/Yellow)
  - Low Risk: `31 <= risk_score <= 60` (Blue)
  - Safe: `risk_score <= 30` (Green)
- Update colors inside the custom HTML5 Canvas doughnut chart to match the mockup visual scheme:
  - High Risk: Red (`#ef4444`)
  - Medium Risk: Yellow/Orange (`#f59e0b`)
  - Low Risk: Blue (`#3b82f6`)
  - Safe: Green (`#10b981`)
- Render the recent scans table with exactly 5 rows containing the items in the mockup:
  - CEO email: `92/100`, Phishing, 2 min ago
  - Amazon typosquat URL: `85/100`, Malicious, 15 min ago
  - deepfake_video.mp4: `88/100`, Deepfake, 30 min ago
  - ignore instructions prompt: `73/100`, Prompt Injection, 45 min ago
  - ai_generated_article.txt: `40/100`, AI-Generated, 1 hr ago
- Clean up any rendering discrepancies in the Canvas drawing context.

#### [MODIFY] [styles.css](file:///C:/Users/PC/.gemini/antigravity/scratch/trustshield-ai/frontend/styles.css)
- Implement high-fidelity styles:
  - Dark mode backgrounds with sleek neon accents (Purple and Teal).
  - Clear glassmorphism (`backdrop-filter`, subtle borders, dark overlays).
  - Custom font setups, padding, and spacing.
  - Hover effects on cards, navigation tabs, and table rows to ensure a highly responsive, premium feel.

---

## Verification Plan

### Automated Verification
- Verify the FastAPI server is running correctly and serving `/` and all `/api/*` endpoints.
- Check the console logs for any Python import or runtime errors.

### Manual Verification
- Launch the browser to verify the layout, typography, and color palette alignment with the mockup.
- Run test scans (e.g. quick scan text, file upload simulations) to verify the composite score math, explanation modal details, and webhook notification toasts.
