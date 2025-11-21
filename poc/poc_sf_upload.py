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
SF_LOGIN_URL = os.getenv("SF_LOGIN_URL", "https://login.salesforce.com")
SF_PRIVATE_KEY_FILE = os.getenv("SF_PRIVATE_KEY_FILE", "./server.key")


def get_jwt_assertion():
    """
    Creates a JWT assertion signed with the private key.
    Returns the JWT as a string.
    """
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
    """
    Exchanges JWT assertion for access token and instance URL.
    Returns (access_token, instance_url).
    """
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
    """
    Creates a Weather_Report__c record.
    Returns Weather_Report__c ID.
    """
    # Example: create a UTC timestamp in ISO8601
    ts = datetime.now(timezone.utc).isoformat()  # "2025-11-21T00:30:12.123456+00:00"
    # Salesforce wants “Z”, not “+00:00”
    ts = ts.replace("+00:00", "Z")

    body = {
        "Name": f"POC Weather Report",
        "Forecast__c": "JWT + simple-salesforce",
        "Import_Timestamp__c": ts,
    }

    return sf.Weather_Report__c.create(body)["id"]


def upload_weather_chart(sf, file_path, record_id):
    """
    Uploads a file as ContentVersion and links it to the given record.
    Returns ContentVersion ID.
    """
    if not os.path.exists(file_path):
        return None

    basename = os.path.basename(file_path)

    with open(file_path, "rb") as f:
        blob = f.read()

    b64 = base64.b64encode(blob).decode("utf-8")

    body = {
        "Title": "Weather Chart",
        "PathOnClient": basename,
        "VersionData": b64,
        "FirstPublishLocationId": record_id,
    }

    return sf.ContentVersion.create(body)["id"]


FILE_PATH = "sample_small.png"

if not os.path.exists(FILE_PATH):
    print(f"{FILE_PATH} not found and aborting.")
    sys.exit(1)

assertion = get_jwt_assertion()
print(f"   JWT assertion: {assertion[:10]}...{assertion[-10:]}")

token, instance = get_token_and_instance(assertion)
print(f"   token: {token[:10]}...{token[-10:]}")
print(f"   instance: {instance}")

sf = Salesforce(instance_url=instance, session_id=token)

wr_record_id = create_weather_report(sf)
print(f"   Weather Report ID: {wr_record_id}")

cv_record_id = upload_weather_chart(sf, FILE_PATH, wr_record_id)
print(f"   Content Version ID: {cv_record_id}")
