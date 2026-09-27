import subprocess
import requests
import json
import os

# 1. Login with session cookie saving using requests session
session = requests.Session()
login_url = "http://127.0.0.1:8000/api/login/"
login_data = {"userName": "john_doe", "password": "Password123!"}
login_res = session.post(login_url, json=login_data)
print(f"Login status: {login_res.status_code}")
print(f"Login response: {login_res.text}")

# Write cookies to Netscape cookie format for curl
cookies_path = r"C:\Projects\jj2\scratch\cookies.txt"
with open(cookies_path, "w") as f:
    f.write("# Netscape HTTP Cookie File\n")
    for cookie in session.cookies:
        f.write(f"127.0.0.1\tFALSE\t/\tFALSE\t0\t{cookie.name}\t{cookie.value}\n")

# 2. Formulate exact cURL command for logout
curl_cmd = "curl -X POST http://127.0.0.1:8000/api/logout/ -b cookies.txt"
curl_exec = ["curl.exe", "-s", "-X", "POST", "http://127.0.0.1:8000/api/logout/", "-b", cookies_path]

# Execute curl command
res = subprocess.run(curl_exec, capture_output=True, text=True)
logout_output = res.stdout.strip()
print(f"Logout output:\n{logout_output}")

# Format logoutuser file content
file_content = f"{curl_cmd}\n{logout_output}\n"

# Write to logoutuser file in root and server/djangoapp
with open(r"C:\Projects\jj2\logoutuser", "w", encoding="utf-8") as f:
    f.write(file_content)

with open(r"C:\Projects\jj2\server\djangoapp\logoutuser", "w", encoding="utf-8") as f:
    f.write(file_content)

print("\n--- SUCCESSFULLY WRITTEN TO logoutuser ---")
