"""
Salesforce OAuth2 (Auth Code + PKCE) Localhost Login

Requires:
- Redirect URI must be *http://localhost:PORT/callback*
  (Salesforce cannot redirect to https or non-local addresses.)

Steps:
1. Open browser to Salesforce OAuth login.
2. Local HTTP server catches the authorization code.
3. Exchange code for access token.
4. Connect via simple_salesforce.
"""

import os
import base64
import hashlib
import secrets
import webbrowser
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

import requests
from simple_salesforce import Salesforce
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("SF_CLIENT_ID")
CLIENT_SECRET = os.getenv("SF_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SF_REDIRECT_URI")  # e.g., http://localhost:8080/callback

PORT = int(REDIRECT_URI.split(":")[2].split("/")[0])


# --------------------------------------------------
# Proof Key for Code Exchange (PKCE) Generator
# --------------------------------------------------
def generate_pkce():
    verifier = base64.urlsafe_b64encode(secrets.token_bytes(40)).rstrip(b"=").decode()
    digest = hashlib.sha256(verifier.encode()).digest()
    challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode()
    method = "S256"
    return verifier, challenge, method


code_verifier, code_challenge, code_challenge_method = generate_pkce()

# --------------------------------------------------
# OAuth URL
# --------------------------------------------------
O_AUTH_URL = (
    "https://login.salesforce.com/services/oauth2/authorize"
    f"?response_type=code"
    f"&client_id={CLIENT_ID}"
    f"&redirect_uri={REDIRECT_URI}"
    f"&code_challenge={code_challenge}"
    f"&code_challenge_method={code_challenge_method}"
)

auth_code = None


# --------------------------------------------------
# HTTP Handler – ignores TLS garbage, handles real GET only
# --------------------------------------------------
class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code

        # Detect TLS ClientHello (HTTPS request to HTTP server)
        if self.requestline.startswith("CONNECT") or self.raw_requestline.startswith(
            b"\x16\x03"
        ):
            print("Received HTTPS request on HTTP server; ignoring.")
            return

        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        auth_code = params.get("code", [None])[0]

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<h2>OAuth Completed. You can close this tab.</h2>")


# --------------------------------------------------
# Server Runner receiving one request only
# --------------------------------------------------
def localhost_wait_for_code():
    with HTTPServer(("127.0.0.1", PORT), OAuthHandler) as httpd:
        print(f"Listening on http://127.0.0.1:{PORT} ...")
        httpd.handle_request()
        time.sleep(0.1)  # tiny delay to avoid race conditions
        print("Server shutting down cleanly.")


# --------------------------------------------------
# Step 1: Open Browser
# --------------------------------------------------
print("Opening browser for Salesforce login...")
webbrowser.open(O_AUTH_URL)

# --------------------------------------------------
# Step 2: LOCAL_HOST waits for browser redirect
# --------------------------------------------------
localhost_wait_for_code()

if not auth_code:
    raise RuntimeError(
        "No authorization code received. Browser likely sent HTTPS instead of HTTP."
    )

print("Authorization Code: " f"{auth_code[:10]}...{auth_code[-10:]}")

# --------------------------------------------------
# Step 3: Exchange code for token
# --------------------------------------------------
TOKEN_URL = "https://login.salesforce.com/services/oauth2/token"

payload = {
    "grant_type": "authorization_code",
    "code": auth_code,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "redirect_uri": REDIRECT_URI,
    "code_verifier": code_verifier,
}

token_response = requests.post(TOKEN_URL, data=payload)
token_response.raise_for_status()
tokens = token_response.json()

access_token = tokens["access_token"]
instance_url = tokens["instance_url"]

print("\nAccess Token: " f"{access_token[:10]}...{access_token[-10:]}")
print("Instance:", instance_url)

# --------------------------------------------------
# Step 4: Connect via simple_salesforce
# --------------------------------------------------
sf = Salesforce(
    session_id=access_token,
    instance_url=instance_url,
)

print("\nConnected as:", sf.sf_instance)
# print("Lead fields:", sf.Lead.describe())  # Very long output
