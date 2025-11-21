import os
from datetime import datetime, timezone
import time
import base64
import jwt
import requests
from dotenv import load_dotenv
from simple_salesforce import Salesforce

load_dotenv()

SF_CLIENT_ID = os.getenv("SF_CLIENT_ID")
SF_USERNAME = os.getenv("SF_USERNAME")
SF_LOGIN_URL = os.getenv("SF_LOGIN_URL")
SF_PRIVATE_KEY_FILE = os.getenv("SF_PRIVATE_KEY_FILE", "./server.key")


def get_jwt_assertion():
    with open(SF_PRIVATE_KEY_FILE, "rb") as f:
        private_key = f.read()

    payload = {
        "iss": SF_CLIENT_ID,
        "sub": SF_USERNAME,
        "aud": SF_LOGIN_URL,
        "exp": int(time.time()) + 180,  # 3 minutes
    }

    return jwt.encode(payload, private_key, algorithm="RS256")


def get_token_and_instance(jwt_assertion):
    token_url = f"{SF_LOGIN_URL}/services/oauth2/token"

    data = {
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": jwt_assertion,
    }

    r = requests.post(token_url, data=data)
    r.raise_for_status()
    resp = r.json()

    return resp["access_token"], resp["instance_url"]


def create_weather_report(sf):
    # Example: create a UTC timestamp in ISO8601
    ts = datetime.now(timezone.utc).isoformat()  # "2025-11-21T00:30:12.123456+00:00"
    # Salesforce wants “Z”, not “+00:00”
    ts = ts.replace("+00:00", "Z")

    body = {
        "Name": f"POC Weather Report",
        "Forecast__c": "JWT + simple-salesforce",
        "Import_Timestamp__c": ts,
    }

    return sf.Weather_Report__c.create(body)


def upload_content(sf, file_path, record_id):
    with open(file_path, "rb") as f:
        blob = f.read()

    b64 = base64.b64encode(blob).decode("utf-8")

    body = {
        "Title": "Weather Chart",
        "PathOnClient": os.path.basename(file_path),
        "VersionData": b64,
        "FirstPublishLocationId": record_id,
    }

    return sf.ContentVersion.create(body)


def main():
    FILE_PATH = "sample_small.png"

    if not os.path.exists(FILE_PATH):
        print(f"{FILE_PATH} not found and aborting.")
        return

    assertion = get_jwt_assertion()
    print(f"   JWT assertion: {assertion[:10]}...{assertion[-10:]}")

    token, instance = get_token_and_instance(assertion)
    print(f"   token: {token[:10]}...{token[-10:]}")
    print(f"   instance: {instance}")

    sf = Salesforce(instance_url=instance, session_id=token)

    wr = create_weather_report(sf)
    wr_record_id = wr["id"]
    print(f"   Weather Report: {wr_record_id}")

    cv = upload_content(sf, FILE_PATH, wr_record_id)
    cv_record_id = cv["id"]
    print(f"   Content Version: {cv_record_id}")

    print("✨ Done.")


if __name__ == "__main__":
    main()
