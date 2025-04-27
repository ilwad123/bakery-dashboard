import time
import subprocess

print("Starting background cron watcher...")

while True:
    print("Checking for due cron jobs...")
    subprocess.run(["python", "manage.py", "runcrons"])
    
    # Wait 5 minutes before checking again
    time.sleep(300)  # 300 seconds = 15 minutes
    print("Waiting for 5 minutes before next check...")