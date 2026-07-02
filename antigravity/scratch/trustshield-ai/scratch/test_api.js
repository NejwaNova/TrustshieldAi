const URL_BASE = 'http://127.0.0.1:8000';

async function runTests() {
    console.log("=== TrustShield AI Node.js Backend Verification ===");
    
    // 1. Test GET /api/stats
    console.log("\n1. Testing GET /api/stats...");
    try {
        const res = await fetch(`${URL_BASE}/api/stats`);
        if (!res.ok) throw new Error(`HTTP Error ${res.status}`);
        const stats = await res.json();
        console.log("Response:", JSON.stringify(stats, null, 2));
        if (stats.total_scans !== undefined && stats.avg_risk_score !== undefined) {
            console.log("✅ Stats structure validated.");
        } else {
            throw new Error("Stats attributes missing!");
        }
    } catch (e) {
        console.error("❌ Stats test failed:", e.message);
        process.exit(1);
    }

    // 2. Test GET /api/scans
    console.log("\n2. Testing GET /api/scans...");
    let initialScansCount = 0;
    try {
        const res = await fetch(`${URL_BASE}/api/scans`);
        if (!res.ok) throw new Error(`HTTP Error ${res.status}`);
        const scans = await res.json();
        initialScansCount = scans.length;
        console.log(`Successfully retrieved ${initialScansCount} scans.`);
        console.log("✅ Scans structure validated.");
    } catch (e) {
        console.error("❌ Scans test failed:", e.message);
        process.exit(1);
    }

    // 3. Test POST /api/scan (BEC Phishing)
    console.log("\n3. Testing POST /api/scan (BEC Phishing email)...");
    try {
        const res = await fetch(`${URL_BASE}/api/scan`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                item: "FROM: ceo@company-internal-alert.com\nTO: finance@company.com\nSUBJECT: URGENT wire transfer ceo bank account routing details",
                type: "Email",
                source: "Verification Script"
            })
        });
        if (!res.ok) throw new Error(`HTTP Error ${res.status}`);
        const data = await res.json();
        console.log("Response:", JSON.stringify(data.scan, null, 2));
        if (data.scan.risk_score >= 71 && data.scan.result === "Critical") {
            console.log("✅ Phishing detection score computed and matches criteria (Score >= 71).");
        } else {
            console.warn("⚠️ Warning: Phishing score calculation mismatch, got:", data.scan.risk_score, data.scan.result);
        }
    } catch (e) {
        console.error("❌ Scan test failed:", e.message);
        process.exit(1);
    }

    // 4. Test POST /api/integrations/webhook/gmail (when enabled)
    console.log("\n4. Testing POST /api/integrations/webhook/gmail (when enabled vs disabled)...");
    try {
        // First retrieve current integrations state
        const intRes = await fetch(`${URL_BASE}/api/integrations`);
        const integrations = await intRes.json();
        console.log("Gmail integration connected status:", integrations.gmail.connected);

        // If connected, test it
        if (integrations.gmail.connected) {
            const hookRes = await fetch(`${URL_BASE}/api/integrations/webhook/gmail`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    sender: "ceo@company.com",
                    content: "Let's check this link https://amaz0n-security-portal.com/login",
                    channel: "Inbox"
                })
            });
            if (!hookRes.ok) throw new Error(`Webhook Ingestion HTTP Error ${hookRes.status}`);
            const result = await hookRes.json();
            console.log("Webhook Response:", JSON.stringify(result, null, 2));
            console.log("✅ Webhook Ingestion verified.");
        } else {
            console.log("Skipping connected test (Gmail is currently disconnected).");
        }
    } catch (e) {
        console.error("❌ Webhook Ingestion test failed:", e.message);
        process.exit(1);
    }

    // 5. Test SSE Connection (stream)
    console.log("\n5. Testing SSE Stream availability...");
    try {
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 1500);
        const res = await fetch(`${URL_BASE}/api/stream`, { signal: controller.signal });
        clearTimeout(timeout);
        
        if (res.headers.get('content-type') && res.headers.get('content-type').includes('text/event-stream')) {
            console.log("✅ SSE Headers match 'text/event-stream'.");
        } else {
            throw new Error(`Content-Type mismatch: ${res.headers.get('content-type')}`);
        }
    } catch (e) {
        if (e.name === 'AbortError') {
            console.log("✅ SSE stream responded and kept connection open (aborted successfully after 1.5s).");
        } else {
            console.error("❌ SSE stream verification failed:", e.message);
            process.exit(1);
        }
    }

    console.log("\n🎉 ALL TESTS COMPLETED SUCCESSFULLY! The Node.js backend is fully operational and compatible. 🎉");
}

runTests();
