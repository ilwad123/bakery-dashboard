import time
import subprocess

print("Starting background cron watcher...")

while True:
    print("Checking for due cron jobs...")
    subprocess.run(["python", "manage.py", "runcrons"])
    
    # Wait 15 minutes before checking again
    time.sleep(900)  # 900 seconds = 15 minutes
    print("Waiting for 15 minutes before next check...")