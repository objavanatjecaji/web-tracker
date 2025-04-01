import time
from datetime import datetime
import sys

print("Starting background worker test...", flush=True)
print("Script initialized", flush=True)

while True:
    current_time = datetime.now()
    current_time_str = current_time.strftime("%H:%M")
    print(f"Running at {current_time_str} UTC", flush=True)
    sys.stdout.flush()  # Osiguraj da se ispisi odmah pojave
    time.sleep(60)
