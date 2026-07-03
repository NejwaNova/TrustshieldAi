import http.client
import json

def verify_new_features():
    conn = http.client.HTTPConnection("127.0.0.1", 8000)
    headers = {"Content-Type": "application/json"}
    
    # 1. Test Login (Invalid Credentials)
    print("Testing POST /api/login with invalid credentials...")
    login_payload_invalid = {"username": "admin", "password": "wrong_password"}
    conn.request("POST", "/api/login", body=json.dumps(login_payload_invalid), headers=headers)
    r1 = conn.getresponse()
    print(f"Status code (expecting 401): {r1.status}")
    if r1.status == 401:
        data = json.loads(r1.read().decode())
        print(f"Success! Correctly returned error: {data['detail']}")
    else:
        print(f"Failed! Received status: {r1.status}")
        return False

    # 2. Test Login (Valid Credentials)
    print("\nTesting POST /api/login with valid credentials...")
    login_payload_valid = {"username": "admin", "password": "admin"}
    conn.request("POST", "/api/login", body=json.dumps(login_payload_valid), headers=headers)
    r2 = conn.getcall = conn.getresponse()
    print(f"Status code (expecting 200): {r2.status}")
    if r2.status == 200:
        data = json.loads(r2.read().decode())
        print("Success! User details:")
        print(json.dumps(data, indent=2))
    else:
        print(f"Failed! Received status: {r2.status}")
        return False

    # 3. Test Subscription Upgrades
    print("\nTesting POST /api/subscription (Upgrading to Enterprise)...")
    sub_payload = {"username": "admin", "plan": "Enterprise Shield"}
    conn.request("POST", "/api/subscription", body=json.dumps(sub_payload), headers=headers)
    r3 = conn.getresponse()
    print(f"Status code (expecting 200): {r3.status}")
    if r3.status == 200:
        data = json.loads(r3.read().decode())
        print("Success! Upgraded user:")
        print(json.dumps(data, indent=2))
    else:
        print(f"Failed! Received status: {r3.status}")
        return False

    print("\nAll new feature API verifications completed successfully!")
    return True

if __name__ == "__main__":
    try:
        verify_new_features()
    except Exception as e:
        print(f"Feature verification failed: {e}")
