import subprocess
import threading
import time
from datetime import datetime, timedelta

# Weilong & Pradosh main contribution

def run_script(script_path):
    try:
        print(f"Running {script_path}")
        process = subprocess.Popen(["/usr/bin/python3", script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            print(f"Error running {script_path}: {stderr.decode('utf-8')}")
        else:
            print(f"Output from {script_path}: {stdout.decode('utf-8')}")

    except Exception as e:
        print(f"Exception occurred: {e}")

def calculate_seconds_until_midnight():
    now = datetime.now()
    midnight = datetime(now.year, now.month, now.day, 0, 0, 0)
    if now > midnight:
        midnight = midnight + timedelta(days=1)
    return (midnight - now).total_seconds()

# List of scripts to launch
scripts = ["gps.py", "oxygen.py", "temperature.py", "cpu_temperature.py", "pressure.py", "sound.py", "wind_speed.py"]

print("Launching scripts...")

# Start each script in a separate thread
for script in scripts:
    thread = threading.Thread(target=run_script, args=("/users/pgrad/srivastp/group24/" + script,))
    thread.start()

# Join threads to prevent the program from exiting immediately
for thread in threading.enumerate():
    if thread != threading.current_thread():
        thread.join()

print("All scripts have completed.")

