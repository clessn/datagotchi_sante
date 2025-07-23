import subprocess
import time
import datetime
import os

LOG_FILE = "download.log"
COMMAND = ["make", "download-files"]
INTERVAL = 30  # seconds

def log_message(message):
    """Append a timestamped message to the log file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")

def run_command():
    """Run the command and log its output."""
    try:
        result = subprocess.run(COMMAND, capture_output=True, text=True, check=True)
        if result.stdout:
            log_message(result.stdout.strip())
        if result.stderr:
            log_message("ERROR: " + result.stderr.strip())
    except subprocess.CalledProcessError as e:
        log_message(f"Command failed with exit code {e.returncode}")
        if e.stdout:
            log_message(e.stdout.strip())
        if e.stderr:
            log_message("ERROR: " + e.stderr.strip())

def main():
    log_message(f"Starting download loop (every {INTERVAL} seconds)...")
    while True:
        run_command()
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
