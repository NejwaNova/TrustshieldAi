import http.client
import json

def test_api():
    conn = http.client.HTTPConnection("127.0.0.1", 8000)
    
    # 1. Test /api/stats
    print("Testing GET /api/stats...")
    conn.request("GET", "/api/stats")
    r1 = conn.getresponse()
    if r1.status == 200:
        data = json.loads(r1.read().decode())
        print("Success! /api/stats response:")
        print(json.dumps(data, indent=2))
    else:
        print(f"Failed! Status code: {r1.status}")
        return False
        
    # 2. Test POST /api/scan
    print("\nTesting POST /api/scan (Quick Scan simulation)...")
    headers = {"Content-Type": "application/json"}
    scan_payload = {
        "item": "https://amaz0n-security-portal.com/login-verification",
        "type": "URL",
        "source": "Web Dashboard"
    }
    conn.request("POST", "/api/scan", body=json.dumps(scan_payload), headers=headers)
    r2 = conn.getresponse()
    if r2.status == 200:
        data = json.loads(r2.read().decode())
        print("Success! /api/scan response:")
        print(f"Risk Score: {data['scan']['risk_score']}, Result: {data['scan']['result']}")
        print(f"Explanation Preview: {data['scan']['details'][:120]}...")
    else:
        print(f"Failed! Status code: {r2.status}")
        return False

    # 3. Test POST /api/integrations/telegram (Connect Telegram)
    print("\nTesting POST /api/integrations/telegram...")
    integration_payload = {
        "connected": True,
        "token": "bot_token_abc123",
        "webhook": ""
    }
    conn.request("POST", "/api/integrations/telegram", body=json.dumps(integration_payload), headers=headers)
    r3 = conn.getcall = conn.getresponse()
    if r3.status == 200:
        data = json.loads(r3.read().decode())
        print("Success! Telegram connected:")
        print(json.dumps(data, indent=2))
    else:
        print(f"Failed! Status code: {r3.status}")
        return False

    # 4. Test POST /api/integrations/webhook/telegram (Simulate voice deepfake webhook)
    print("\nTesting POST /api/integrations/webhook/telegram...")
    webhook_payload = {
        "sender": "@malicious_bot",
        "content": "[Forwarded Audio Memo Attachment] cloned_ceo_voice_authorization.wav",
        "channel": "Direct Bot",
        "attachment_name": "cloned_voice_memo.wav"
    }
    conn.request("POST", "/api/integrations/webhook/telegram", body=json.dumps(webhook_payload), headers=headers)
    r4 = conn.getresponse()
    if r4.status == 200:
        data = json.loads(r4.read().decode())
        print("Success! Webhook processed:")
        print(json.dumps(data, indent=2))
    else:
        print(f"Failed! Status code: {r4.status}")
        return False
        
    print("\nAll backend API tests completed successfully! Verification PASSED.")
    return True

if __name__ == "__main__":
    try:
        test_api()
    except Exception as e:
        print(f"API request failed: {e}")
