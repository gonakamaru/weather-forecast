"""
Salesforce OAuth2 (JWT Bearer) Login — No Browser, No Redirect

Flow:
1. Build a signed JWT assertion using your private key.
2. Send it to Salesforce's /token endpoint with grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer
3. Receive access token.
4. Connect via simple_salesforce.

Requires:
- Connected App with certificate uploaded.
- User approved for the Connected App.
"""

import os
import time
import json
import base64
import jwt  # PyJWT
import requests
from simple_salesforce import Salesforce
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("SF_CLIENT_ID")
USERNAME = os.getenv("SF_USERNAME")  # The user to impersonate
AUDIENCE = os.getenv("SF_AUDIENCE", "https://login.salesforce.com")
PRIVATE_KEY_PATH = os.getenv("SF_PRIVATE_KEY_PATH")

# --------------------------------------------------
# Load private key
# --------------------------------------------------
with open(PRIVATE_KEY_PATH, "rb") as f:
    PRIVATE_KEY = f.read()


# --------------------------------------------------
# Create JWT assertion
# --------------------------------------------------
def create_jwt_assertion():
    now = int(time.time())
    exp = now + 300  # 5 minutes
    payload = {
        "iss": CLIENT_ID,
        "sub": USERNAME,
        "aud": AUDIENCE,
        "exp": exp,
    }
    assertion = jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")
    return assertion


jwt_assertion = create_jwt_assertion()

# --------------------------------------------------
# Exchange JWT for Access Token
# --------------------------------------------------
TOKEN_URL = f"{AUDIENCE}/services/oauth2/token"

payload = {
    "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
    "assertion": jwt_assertion,
}

response = requests.post(TOKEN_URL, data=payload)
response.raise_for_status()

tokens = response.json()
access_token = tokens["access_token"]
instance_url = tokens["instance_url"]

print("\nAccess Token:", f"{access_token[:12]}...{access_token[-12:]}")
print("Instance:", instance_url)

# --------------------------------------------------
# Connect via simple_salesforce
# --------------------------------------------------
sf = Salesforce(
    session_id=access_token,
    instance_url=instance_url,
)

print("\nConnected as:", sf.sf_instance)
