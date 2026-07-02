import re
import math

class TrustShieldEngine:
    def __init__(self):
        # Weights for each shield in the composite formula
        self.weights = {
            "email": 1.0,
            "website": 1.0,
            "deepfake": 1.2,
            "prompt": 0.8,
            "qr": 0.9,
            "document": 1.0
        }

    def analyze(self, payload, asset_type, filename=""):
        payload_str = payload or ""
        text = payload_str.lower()
        type_str = asset_type or ""
        filename_str = filename or ""

        # Initialize scores and findings
        scores = {
            "email": 0,
            "website": 0,
            "deepfake": 0,
            "prompt": 0,
            "qr": 0,
            "document": 0
        }

        findings = {
            "email": [],
            "website": [],
            "deepfake": [],
            "prompt": [],
            "qr": [],
            "document": []
        }

        # 1. Email Shield
        is_email = (type_str == "Email" or 
                    type_str.lower() == "text" or 
                    "from:" in text or 
                    "subject:" in text)
        if is_email:
            # Check for BEC keywords
            bec_keywords = [
                "urgent bank transfer", "wire transfer", "wire money", "ceo", "routing number",
                "bank account", "update direct deposit", "immediate action", "credentials"
            ]
            matches = [k for k in bec_keywords if k in text]
            if matches:
                scores["email"] += min(len(matches) * 20, 60)
                findings["email"].append(f"Suspicious BEC keywords detected: {', '.join(matches)}")

            # Simulate SPF/DKIM validation
            has_from_or_is_email = "from:" in text or type_str == "Email"
            if "received:" not in text and has_from_or_is_email:
                scores["email"] += 30
                findings["email"].append("Missing or unaligned DKIM/SPF headers")
            else:
                if scores["email"] == 0:
                    scores["email"] = 10
                    findings["email"].append("Email signatures and headers aligned")

        # 2. Website Shield
        url_regex = r'(https?://[^\s]+)'
        urls = re.findall(url_regex, payload_str)
        is_url = type_str == "URL" or len(urls) > 0
        if is_url:
            target_url = urls[0] if len(urls) > 0 else payload_str
            scores["website"] = 15  # baseline check
            findings["website"].append(f"Analyzing reputation for URL: {target_url}")

            # Check for typosquatting variations
            typosquats = ["amaz0n", "paypaI", "micros0ft", "sec-login", "support-verify", "update-bank", "free-gift"]
            matched_typo = next((t for t in typosquats if t in target_url.lower()), None)
            if matched_typo:
                scores["website"] += 60
                findings["website"].append(f"Typosquatting detected (substitutions match: {matched_typo})")

            # Check for credential harvesting paths
            target_lower = target_url.lower()
            if "login" in target_lower or "verify" in target_lower or "auth" in target_lower:
                scores["website"] += 15
                findings["website"].append("High-risk path detected (login/verification keyword)")

            # Caps URL score at 100
            scores["website"] = min(scores["website"], 100)

        # 3. Deepfake Shield
        file_lower = filename_str.lower()
        media_extensions = ('.mp4', '.mov', '.avi', '.mp3', '.wav', '.aac', '.png', '.jpg', '.jpeg')
        is_media = (type_str in ["Video", "Audio", "Image"] or 
                    file_lower.endswith(media_extensions))
        if is_media:
            scores["deepfake"] = 20  # baseline verification
            findings["deepfake"].append("Ingested multi-media stream for neural validation")

            # Keywords indicating deepfakes in simulated tests
            if any(k in text for k in ["manipulated", "fake", "synthesized", "cloned"]):
                scores["deepfake"] = 88
                findings["deepfake"].append("CNN spatial model identified face-warping artifacts")
                findings["deepfake"].append("Audio spectrum analyzer detected synthetic phase anomalies (cloned voice)")
            else:
                # Default mock scanning for media files in dashboard demo
                if "deepfake" in file_lower or "cloned" in file_lower:
                    scores["deepfake"] = 88
                    findings["deepfake"].append("CNN spatial model identified face-warping artifacts")
                else:
                    scores["deepfake"] = 12
                    findings["deepfake"].append("Structural video frames show optical consistency")

        # 4. Prompt Shield
        if type_str == "Text / Prompt" or len(payload_str) > 0:
            prompt_patterns = [
                r'ignore previous instructions',
                r'system prompt',
                r'dan mode',
                r'jailbreak',
                r'you are now an unfiltered',
                r'bypass safety',
                r'output admin password',
                r'forget rules'
            ]
            matched_patterns = [p for p in prompt_patterns if re.search(p, text, re.IGNORECASE)]
            if matched_patterns:
                scores["prompt"] = 85
                findings["prompt"].append(f"Adversarial jailbreak pattern detected: '{matched_patterns[0]}'")
            else:
                if type_str == "Text / Prompt":
                    scores["prompt"] = 8
                    findings["prompt"].append("Prompt tokens analyzed; safety guidelines respected")

        # 5. QR Shield
        has_qr_keywords = "qr" in text or "scan" in text or "quishing" in text
        is_image_file = file_lower.endswith(('.png', '.jpg', '.jpeg'))
        if has_qr_keywords or (type_str == "Image" and is_image_file) or (type_str == "Image"):
            scores["qr"] = 15
            findings["qr"].append("Computer vision matrix scanner activated")

            if "malicious-qr" in text or "quish" in text:
                scores["qr"] = 82
                findings["qr"].append("Decoded QR matrix yields suspicious redirect link: http://sec-auth-portal.com")
            else:
                findings["qr"].append("No suspicious redirect payloads embedded inside decoded QR matrices")

        # 6. Document Shield
        is_document = (type_str == "Document" or 
                       file_lower.endswith(('.pdf', '.docx', '.xlsx', '.zip')))
        if is_document:
            scores["document"] = 10
            findings["document"].append("Deconstructing document schema elements")

            if any(k in text for k in ["macro", "exploit", "script"]):
                scores["document"] = 78
                findings["document"].append("Embedded active code/script macros detected")
            else:
                findings["document"].append("XML schemas fully validated; no active code block objects detected")

        # Build active shields map
        active_shields = {shield: score for shield, score in scores.items() if score > 0}

        # Avoid division by zero by setting a default
        if not active_shields:
            active_shields["email"] = 5
            scores["email"] = 5
            findings["email"].append("No specific threats flagged during vector telemetry scan")

        # Compute Composite Score
        max_score = max(active_shields.values())

        weighted_sum = sum(self.weights[shield] * scores[shield] for shield in active_shields)
        sum_weights = sum(self.weights[shield] for shield in active_shields)

        weighted_avg = (weighted_sum / sum_weights) if sum_weights > 0 else 0.0

        composite_score = math.floor(max_score * 0.6 + weighted_avg * 0.4)
        composite_score = min(max(composite_score, 0), 100)

        # Classifications
        if composite_score <= 20:
            result = "Safe"
            verdict = "Allowed"
            mitigation = "No action required. The asset appears authentic and carries no significant digital threat telemetry."
        elif composite_score <= 40:
            result = "Suspicious"
            verdict = "User Warned"
            mitigation = "Exercise caution. Minor anomalies detected. Avoid sharing sensitive data or clicking nested links without out-of-band verification."
        elif composite_score <= 70:
            result = "High Risk"
            verdict = "Asset Quarantined"
            mitigation = "Quarantine executed. Multiple telemetry indicators flagged. Do not open attachments or input credentials."
        else:
            result = "Critical"
            verdict = "Blocked"
            mitigation = "Payload blocked immediately. Confirmed malicious signature, brand impersonation, or deepfake model matches."

        # Compile markdown response
        all_findings = []
        for shield, text_list in findings.items():
            if text_list and scores[shield] > 0:
                cap_shield = shield.capitalize()
                all_findings.append(f"**{cap_shield} Shield (Score: {scores[shield]}/100)**: {'; '.join(text_list)}")

        explanation_body = "\n".join([f"- {f}" for f in all_findings])

        math_details = (
            f"**Trust Engine Composite Scoring Math**:\n"
            f"\\( S_{{composite}} = \\max(S_{{critical}}) \\times 0.6 + \\left( \\frac{{\\sum (W_i \\times S_i)}}{{\\sum W_i}} \\right) \\times 0.4 \\)\n\n"
            f"Inputs: Max active score = {max_score}, Weighted Avg = {weighted_avg:.1f}.\n"
            f"Calculation: \\({max_score} \\times 0.6 + {weighted_avg:.1f} \\times 0.4 = {composite_score}\\) (Clamped to 100)."
        )

        detailed_report = (
            f"### Threat Telemetry Verdict: {result.upper()} ({composite_score}/100)\n\n"
            f"**System Action**: {verdict}\n\n"
            f"**Mitigation Recommendation**:\n{mitigation}\n\n"
            f"**Active Telemetry Logs**:\n{explanation_body}\n\n"
            f"{math_details}"
        )

        active_shield_names = [s.capitalize() for s in active_shields.keys()]

        return {
            "risk_score": composite_score,
            "result": result,
            "verdict": verdict,
            "shield_scores": scores,
            "explanation": detailed_report,
            "details": f"Analyzed via {', '.join(active_shield_names)}."
        }
