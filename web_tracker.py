import time
from datetime import datetime

print("Starting background worker test...")
print("Script initialized")

while True:
    current_time = datetime.now()
    current_time_str = current_time.strftime("%H:%M")
    print(f"Running at {current_time_str} UTC")
    time.sleep(60)  # Čekaj 1 minutu između ispisa
