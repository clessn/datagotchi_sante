import datetime
import os
import subprocess
import sys
import time

from dotenv import load_dotenv

LOG_FILE = "regular.log"
INTERVAL = 10  # seconds

# Load environment variables from .env file (in the script's directory or above)
load_dotenv()


def log_message(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")


def run_command(command_str):
    """Run the given shell command and log its output."""
    try:
        result = subprocess.run(
            command_str, shell=True, capture_output=True, text=True, check=True
        )
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
    if len(sys.argv) < 2:
        print("Usage: python regular_runner.py '<command>'")
        sys.exit(1)

    command_str = " ".join(sys.argv[1:])
    log_message(
        f"Starting regular loop (every {INTERVAL} seconds) for command: {command_str}"
    )

    while True:
        run_command(command_str)
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
