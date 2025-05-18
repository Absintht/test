import sys
import requests
import json

APP_NAME = "Lynx loader"
APP_VERSION = "1.0"
OWNER_ID = "6PlQvoXHNZ"
APP_KEY = "test"

def notify(msg):
    print(f"[{APP_NAME}] {msg}")

def keyauth_get(params):
    url = f"https://keyauth.win/api/1.1/?{params}"
    response = requests.get(url)
    return response.json()

def init_keyauth():
    params = f"name={APP_KEY}&ownerid={OWNER_ID}&type=init&ver={APP_VERSION}"
    data = keyauth_get(params)
    if not data or not data.get("success", False):
        notify("Initialization failed.")
        return None
    if data.get("message") == "invalidver":
        notify("Error: Wrong application version.")
        return None
    return data.get("sessionid")

def check_license(sessionid, license_key):
    params = f"name={APP_KEY}&ownerid={OWNER_ID}&type=license&key={license_key}&ver={APP_VERSION}&sessionid={sessionid}"
    data = keyauth_get(params)
    if not data or not data.get("success", False):
        notify(f"License error: {data.get('message', 'Unknown error')}")
        return False
    # Save result to file
    with open("auth_data.json", "w") as f:
        json.dump(data, f)
    notify("Successfully logged in!")
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python auth.py LICENSE_KEY")
        sys.exit(1)
    license_key = sys.argv[1]
    sessionid = init_keyauth()
    if not sessionid:
        sys.exit(2)
    success = check_license(sessionid, license_key)
    if success:
        sys.exit(0)
    else:
        sys.exit(3)

if __name__ == "__main__":
    main()
