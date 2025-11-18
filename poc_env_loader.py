#!/usr/bin/env python3
from dotenv import load_dotenv
import os

load_dotenv()

print("SF_USERNAME =", os.getenv("SF_USERNAME"))
print("SF_DOMAIN   =", os.getenv("SF_DOMAIN"))
