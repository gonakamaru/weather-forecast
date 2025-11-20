#!/usr/bin/env python3
"""
Salesforce JWT Bearer Flow Authentication

Requires:
- Enable JWT Bearer Flow in Connected App settings
- Create RSA key pair, upload public key to Connected App
"""

import os
import time
import jwt
import requests
from dotenv import load_dotenv

# Load env variables
load_dotenv()

SF_CLIENT_ID = os.getenv("SF_CLIENT_ID")  # Connected App Consumer Key
SF_USERNAME = os.getenv("SF_USERNAME")  # Salesforce username
JWT_KEY_PATH = os.getenv("SF_JWT_PRIVATE_KEY")  # Path to private key file
SF_LOGIN_URL = "https://login.salesforce.com/services/oauth2/token"


def build_jwt_assertion():
    # Create JWT assertion signed with RSA private key.
    with open(JWT_KEY_PATH, "r") as f:
        private_key = f.read()

    now = int(time.time())
    exp = now + 300  # 5 minutes (JWT max recommended)

    payload = {
        "iss": SF_CLIENT_ID,  # client_id
        "sub": SF_USERNAME,  # username
        "aud": "https://login.salesforce.com",  # audience
        "exp": exp,
    }

    assertion = jwt.encode(payload, private_key, algorithm="RS256")

    return assertion


def get_access_token(assertion):
    # Exchange the JWT assertion for an access token.

    data = {
        "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        "assertion": assertion,
    }

    response = requests.post(SF_LOGIN_URL, data=data)

    if response.status_code != 200:
        raise RuntimeError(f"JWT auth failed: {response.text}")

    token_data = response.json()
    return token_data["access_token"], token_data["instance_url"]


print("Authenticating with Salesforce using JWT...")

assertion = build_jwt_assertion()
access_token, instance_url = get_access_token(assertion)

print("Access Token: " f"{access_token[:10]}...{access_token[-10:]}")
print("Instance URL:", instance_url)

# describe Lead object
r = requests.get(
    f"{instance_url}/services/data/v59.0/sobjects/Lead/describe",
    headers={"Authorization": f"Bearer {access_token}"},
)

print("Lead Describe Status:", r.status_code)
print(r.json())

# --------------------------------------------------
# Connect via simple_salesforce
# --------------------------------------------------
sf = Salesforce(
    session_id=access_token,
    instance_url=instance_url,
)

print("\nConnected as:", sf.sf_instance)
# print("Lead fields:", sf.Lead.describe())  # Very long output
