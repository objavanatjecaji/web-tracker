import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

EMAIL = "objava.natjecaji10@gmail.com"
PASSWORD = "triqsjwgvpnhmzzt"
TO_EMAIL = "objava.natjecaji10@gmail.com"
CHECK_INTERVAL = 1200
REPORT_TIMES = ["12:05", "14:05", "18:05", "21:05"]

sent_reports = {time: False for time in REPORT_TIMES}
last_reset = datetime.now().date()

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL
    msg['To'] = TO_EMAIL
    try:
        print("Sending email...")
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)
            print(f"E-mail poslan u {datetime.now().strftime('%H:%M')}")
    except Exception as e:
        print(f"Greška pri slanju e-maila: {e}")

print("Script started successfully")
while True:
    current_time = datetime.now()
    current_time_str = current_time.strftime("%H:%M")
    print(f"Running at {current_time_str}")

    if current_time.date() != last_reset:
        sent_reports = {time: False for time in REPORT_TIMES}
        last_reset = current_time.date()
        print("Resetting sent_reports")

    for report_time in REPORT_TIMES:
        report_hour, report_minute = map(int, report_time.split(":"))
        report_datetime = current_time.replace(hour=report_hour, minute=report_minute, second=0, microsecond=0)
        if current_time >= report_datetime and not sent_reports[report_time]:
            send_email(f"Test izvještaj ({report_time})", "Test email from Render")
            sent_reports[report_time] = True

    print(f"Sleeping for {CHECK_INTERVAL} seconds...")
    time.sleep(CHECK_INTERVAL)
