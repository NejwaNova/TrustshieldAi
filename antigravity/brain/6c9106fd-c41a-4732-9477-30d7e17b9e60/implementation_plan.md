# Implementation Plan - Subscription, Amharic Language, and Login Features

Enhance the TrustShield AI platform with three essential features:
1. **Operator Login Flow**: Full authentication overlay preventing unauthorized dashboard access.
2. **Amharic Language Toggle**: A clean localization switcher translating landing elements and dashboard nodes.
3. **Subscription & Pricing Panel**: Interactive tiers (Free, Pro, Enterprise) modifying scanning limits and features list.

---

## Proposed Changes

### Frontend Configuration

#### [MODIFY] [index.html](file:///C:/Users/PC/.gemini/antigravity/scratch/trustshield-ai/frontend/index.html)
- Add Language Switcher toggle (English / Amharic) in the header.
- Add "Operator Login" button in the landing page header.
- Add full-page glassmorphic login screen overlay (`#login-overlay`) with modern glowing form elements.
- Add a new "Subscription" nav tab in the dashboard sidebar.
- Add `#tab-subscription` layout containing three premium pricing cards with custom gradients and plan listings.
- Inject `data-translate` markers on all localizable headings, text blocks, and buttons.

#### [MODIFY] [app.js](file:///C:/Users/PC/.gemini/antigravity/scratch/trustshield-ai/frontend/app.js)
- Add `LOCALIZATION` dictionary mapping key elements between English and Amharic.
- Implement `setLanguage(lang)` function to dynamically translate labeled elements and update placeholders.
- Add session login state. Secure check against backend `POST /api/login`.
- Manage login visibility and block dashboard tabs for unauthenticated operators.
- Implement `selectPlan(planName)` function calling `POST /api/subscription`, upgrading the active operator profile, and updating the dashboard header.

#### [MODIFY] [styles.css](file:///C:/Users/PC/.gemini/antigravity/scratch/trustshield-ai/frontend/styles.css)
- Style the Language Switcher button toggles.
- Add styling for the Login screen overlay: glassmorphic card, glowing input fields, password visibility toggles, and login container slide-in animations.
- Add styling for the Subscription grid and pricing cards (glow accents, list icons, plan badge, hover lift transitions).

---

### Backend Logic & Persistence

#### [MODIFY] [database.py](file:///C:/Users/PC/.gemini/antigravity/scratch/trustshield-ai/backend/database.py)
- Expand database file (`db_store.json`) with operator session store and subscription tier logs.
- Add helper method `set_subscription(user_id, plan_name)` and login verification logging.

#### [MODIFY] [server.py](file:///C:/Users/PC/.gemini/antigravity/scratch/trustshield-ai/backend/server.py)
- Create `POST /api/login` endpoint verifying operator credentials (default: username `admin`, password `admin`).
- Create `POST /api/subscription` endpoint upgrading subscription plan.

---

## Verification Plan

### Manual Verification
1. **Localization Check**: Click the "አማ" (Amharic) button and verify major parts of the landing page and dashboard translate instantly. Click "EN" to return to English.
2. **Login Verification**: Try clicking "View Dashboard" or sidebar buttons before logging in; verify it forces the login overlay. Log in with `admin` / `admin` and check smooth slide-out and dashboard unlocking.
3. **Subscription Upgrades**: Go to "Subscription" tab, select "Pro Shield" or "Enterprise Shield", click "Select Plan", verify toast notification and operators details updating.
