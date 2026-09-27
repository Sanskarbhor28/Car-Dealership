import subprocess
import time
import os
import sys

cmd = [sys.executable, "manage.py", "runserver", "8000"]
env = os.environ.copy()

proc = subprocess.Popen(
    cmd,
    cwd=r"C:\Projects\jj2\server\djangoapp",
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1
)

lines = []
start_time = time.time()

# Read output until server is started or 5 seconds timeout
while time.time() - start_time < 5:
    line = proc.stdout.readline()
    if line:
        lines.append(line)
        print(line, end="")
        if "Quit the server with" in line or "Press CTRL-BREAK" in line or "http://127.0.0.1:8000/" in line:
            break

output_text = "".join(lines)

# Save output to django_server file in root and server/djangoapp
with open(r"C:\Projects\jj2\django_server", "w", encoding="utf-8") as f:
    f.write(output_text)

with open(r"C:\Projects\jj2\server\djangoapp\django_server", "w", encoding="utf-8") as f:
    f.write(output_text)

print("\n--- CAPTURED TERMINAL OUTPUT SAVED TO django_server ---")
