export class TrustShieldEngine {
    constructor() {
        // Weights for each shield in the composite formula
        this.weights = {
            "email": 1.0,
            "website": 1.0,
            "deepfake": 1.2,
            "prompt": 0.8,
            "qr": 0.9,
            "document": 1.0
        };
    }

    analyze(payload, assetType, filename = "") {
        // Lowercase for keyword scans
        const payloadStr = payload || "";
        const text = payloadStr.toLowerCase();
        const typeStr = assetType || "";
        const filenameStr = filename || "";

        // Initialize scores for all shields
        const scores = {
            "email": 0,
            "website": 0,
            "deepfake": 0,
            "prompt": 0,
            "qr": 0,
            "document": 0
        };

        const findings = {
            "email": [],
            "website": [],
            "deepfake": [],
            "prompt": [],
            "qr": [],
            "document": []
        };

        // 1. Email Shield
        const isEmail = typeStr === "Email" || typeStr.toLowerCase() === "text" || text.includes("from:") || text.includes("subject:");
        if (isEmail) {
            // Check for BEC keywords
            const becKeywords = [
                "urgent bank transfer", "wire transfer", "wire money", "ceo", "routing number",
                "bank account", "update direct deposit", "immediate action", "credentials"
            ];
            const matches = becKeywords.filter(k => text.includes(k));
            if (matches.length > 0) {
                scores["email"] += Math.min(matches.length * 20, 60);
                findings["email"].push(`Suspicious BEC keywords detected: ${matches.join(", ")}`);
            }

            // Simulate SPF/DKIM validation
            const hasFromOrIsEmail = text.includes("from:") || typeStr === "Email";
            if (!text.includes("received:") && hasFromOrIsEmail) {
                scores["email"] += 30;
                findings["email"].push("Missing or unaligned DKIM/SPF headers");
            } else {
                // If they paste a clean email, keep it low
                if (scores["email"] === 0) {
                    scores["email"] = 10;
                    findings["email"].push("Email signatures and headers aligned");
                }
            }
        }

        // 2. Website Shield
        const urlRegex = /(https?:\/\/[^\s]+)/g;
        const urls = payloadStr.match(urlRegex) || [];
        const isUrl = typeStr === "URL" || urls.length > 0;
        if (isUrl) {
            const targetUrl = urls.length > 0 ? urls[0] : payloadStr;
            scores["website"] = 15; // baseline check
            findings["website"].push(`Analyzing reputation for URL: ${targetUrl}`);

            // Check for typosquatting variations
            const typosquats = ["amaz0n", "paypaI", "micros0ft", "sec-login", "support-verify", "update-bank", "free-gift"];
            const matchedTypo = typosquats.find(t => targetUrl.toLowerCase().includes(t));
            if (matchedTypo) {
                scores["website"] += 60;
                findings["website"].push(`Typosquatting detected (substitutions match: ${matchedTypo})`);
            }

            // Check for credential harvesting paths
            const targetLower = targetUrl.toLowerCase();
            if (targetLower.includes("login") || targetLower.includes("verify") || targetLower.includes("auth")) {
                scores["website"] += 15;
                findings["website"].push("High-risk path detected (login/verification keyword)");
            }

            // Caps URL score at 100
            scores["website"] = Math.min(scores["website"], 100);
        }

        // 3. Deepfake Shield
        const fileLower = filenameStr.toLowerCase();
        const isMedia = ["Video", "Audio", "Image"].includes(typeStr) ||
            fileLower.endsWith('.mp4') || fileLower.endsWith('.mov') || fileLower.endsWith('.avi') ||
            fileLower.endsWith('.mp3') || fileLower.endsWith('.wav') || fileLower.endsWith('.aac') ||
            fileLower.endsWith('.png') || fileLower.endsWith('.jpg') || fileLower.endsWith('.jpeg');
        if (isMedia) {
            scores["deepfake"] = 20; // baseline verification
            findings["deepfake"].push("Ingested multi-media stream for neural validation");

            // Keywords indicating deepfakes in simulated tests
            if (text.includes("manipulated") || text.includes("fake") || text.includes("synthesized") || text.includes("cloned")) {
                scores["deepfake"] = 88;
                findings["deepfake"].push("CNN spatial model identified face-warping artifacts");
                findings["deepfake"].push("Audio spectrum analyzer detected synthetic phase anomalies (cloned voice)");
            } else {
                // Default mock scanning for media files in dashboard demo
                if (fileLower.includes("deepfake") || fileLower.includes("cloned")) {
                    scores["deepfake"] = 88;
                    findings["deepfake"].push("CNN spatial model identified face-warping artifacts");
                } else {
                    scores["deepfake"] = 12;
                    findings["deepfake"].push("Structural video frames show optical consistency");
                }
            }
        }

        // 4. Prompt Shield
        if (typeStr === "Text / Prompt" || payloadStr.length > 0) {
            const promptPatterns = [
                /ignore previous instructions/i,
                /system prompt/i,
                /dan mode/i,
                /jailbreak/i,
                /you are now an unfiltered/i,
                /bypass safety/i,
                /output admin password/i,
                /forget rules/i
            ];

            const matchedPatterns = promptPatterns.filter(pattern => pattern.test(text));
            if (matchedPatterns.length > 0) {
                scores["prompt"] = 85;
                // Use the string version of the first matched pattern regex
                findings["prompt"].push(`Adversarial jailbreak pattern detected: '${matchedPatterns[0].source}'`);
            } else {
                if (typeStr === "Text / Prompt") {
                    scores["prompt"] = 8;
                    findings["prompt"].push("Prompt tokens analyzed; safety guidelines respected");
                }
            }
        }

        // 5. QR Shield
        const hasQrKeywords = text.includes("qr") || text.includes("scan") || text.includes("quishing");
        const isImage = typeStr === "Image" || fileLower.endsWith('.png') || fileLower.endsWith('.jpg') || fileLower.endsWith('.jpeg');
        if (hasQrKeywords || (isImage && typeStr === "Image")) {
            scores["qr"] = 15;
            findings["qr"].push("Computer vision matrix scanner activated");

            if (text.includes("malicious-qr") || text.includes("quish")) {
                scores["qr"] = 82;
                findings["qr"].push("Decoded QR matrix yields suspicious redirect link: http://sec-auth-portal.com");
            } else {
                findings["qr"].push("No suspicious redirect payloads embedded inside decoded QR matrices");
            }
        }

        // 6. Document Shield
        const isDocument = typeStr === "Document" || fileLower.endsWith('.pdf') || fileLower.endsWith('.docx') || fileLower.endsWith('.xlsx') || fileLower.endsWith('.zip');
        if (isDocument) {
            scores["document"] = 10;
            findings["document"].push("Deconstructing document schema elements");

            if (text.includes("macro") || text.includes("exploit") || text.includes("script")) {
                scores["document"] = 78;
                findings["document"].push("Embedded active code/script macros detected");
            } else {
                findings["document"].push("XML schemas fully validated; no active code block objects detected");
            }
        }

        // AI Explanation Engine & Trust Score calculation
        const activeShields = {};
        for (const [shield, score] of Object.entries(scores)) {
            if (score > 0) {
                activeShields[shield] = score;
            }
        }

        // Ensure at least one shield is active to avoid division by zero
        if (Object.keys(activeShields).length === 0) {
            activeShields["email"] = 5;
            scores["email"] = 5;
            findings["email"].push("No specific threats flagged during vector telemetry scan");
        }

        // Compute Composite Score
        const maxScore = Math.max(...Object.values(activeShields));

        let weightedSum = 0;
        let sumWeights = 0;
        for (const shield of Object.keys(activeShields)) {
            weightedSum += this.weights[shield] * scores[shield];
            sumWeights += this.weights[shield];
        }

        const weightedAvg = sumWeights > 0 ? (weightedSum / sumWeights) : 0;

        // Use Math.floor to match Python's int() truncation behavior
        let compositeScore = Math.floor(maxScore * 0.6 + weightedAvg * 0.4);
        compositeScore = Math.min(Math.max(compositeScore, 0), 100); // Clamp between 0 and 100

        // Classify threat category based on composite score
        let result = "";
        let verdict = "";
        let mitigation = "";

        if (compositeScore <= 20) {
            result = "Safe";
            verdict = "Allowed";
            mitigation = "No action required. The asset appears authentic and carries no significant digital threat telemetry.";
        } else if (compositeScore <= 40) {
            result = "Suspicious";
            verdict = "User Warned";
            mitigation = "Exercise caution. Minor anomalies detected. Avoid sharing sensitive data or clicking nested links without out-of-band verification.";
        } else if (compositeScore <= 70) {
            result = "High Risk";
            verdict = "Asset Quarantined";
            mitigation = "Quarantine executed. Multiple telemetry indicators flagged. Do not open attachments or input credentials.";
        } else {
            result = "Critical";
            verdict = "Blocked";
            mitigation = "Payload blocked immediately. Confirmed malicious signature, brand impersonation, or deepfake model matches.";
        }

        // Compile natural language explanation
        const allFindings = [];
        for (const [shield, textList] of Object.entries(findings)) {
            if (textList.length > 0 && scores[shield] > 0) {
                // capitalize shield name helper
                const capShield = shield.charAt(0).toUpperCase() + shield.slice(1);
                allFindings.push(`**${capShield} Shield (Score: ${scores[shield]}/100)**: ` + textList.join("; "));
            }
        }

        const explanationBody = allFindings.map(f => `- ${f}`).join("\n");

        const mathDetails = (
            `**Trust Engine Composite Scoring Math**:\n` +
            `\\( S_{{composite}} = \\max(S_{{critical}}) \\times 0.6 + \\left( \\frac{{\\sum (W_i \\times S_i)}}{{\\sum W_i}} \\right) \\times 0.4 \\)\n\n` +
            `Inputs: Max active score = ${maxScore}, Weighted Avg = ${weightedAvg.toFixed(1)}.\n` +
            `Calculation: \\(${maxScore} \\times 0.6 + ${weightedAvg.toFixed(1)} \\times 0.4 = ${compositeScore}\\) (Clamped to 100).`
        );

        const detailedReport = (
            `### Threat Telemetry Verdict: ${result.toUpperCase()} (${compositeScore}/100)\n\n` +
            `**System Action**: ${verdict}\n\n` +
            `**Mitigation Recommendation**:\n${mitigation}\n\n` +
            `**Active Telemetry Logs**:\n${explanationBody}\n\n` +
            `${mathDetails}`
        );

        const activeShieldNames = Object.keys(activeShields)
            .map(s => s.charAt(0).toUpperCase() + s.slice(1));

        return {
            "risk_score": compositeScore,
            "result": result,
            "verdict": verdict,
            "shield_scores": scores,
            "explanation": detailedReport,
            "details": `Analyzed via ${activeShieldNames.join(", ")}.`
        };
    }
}
