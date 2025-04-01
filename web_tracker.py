import requests
from bs4 import BeautifulSoup
import time
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import json
import sys

URLS = [
    "https://www.opcina-cadjavica.hr/downloads/natjecaj/",
    "https://novi-vinodolski.hr/",
    "https://www.mikanovci.hr/",
    "https://gorica.hr/",
    "https://www.dnz.hr/category/upravni-odjeli/za-poljoprivredu-i-ruralni-razvoj/",
    "https://zagreb.hr/natjecaji/860",
    "https://ozalj.hr/natjecaji/javni-pozivi/",
    "http://www.rakovica.hr/novosti",
    "https://lag-sredisnjaistra.hr/",
    "https://lag-zrinskagora-turopolje.hr/lag-natjecaji/",
    "https://lagzs.com/novosti/",
    "https://www.srijem.info/index.php?list=natjecaji",
    "https://lag-strossmayer.hr/novosti/",
    "https://lag-una.hr/",
    "https://www.lag-sjevernaistra.hr/aktivni/",
    "https://www.lag-laura.hr/novosti/",
    "https://www.kvarnerski-otoci.hr/natjecaji",
    "https://www.lag-juznaistra.hr/otvoreni-natjecaji",
    "https://www.lag-gorskikotar.hr/",
    "http://lag-istocnaistra.hr/novosti/",
    "https://www.lag-izvor.eu/"
]
EMAIL = "objava.natjecaji10@gmail.com"
PASSWORD = "triqsjwgvpnhmzzt"
TO_EMAIL = "objava.natjecaji10@gmail.com"
CHECK_INTERVAL = 1200  # 20 minutes
REPORT_TIMES = ["10:05", "12:05", "16:05", "19:05"]  # UTC za CEST 12:05, 14:05, 18:05, 21:05

print("Starting script...", flush=True)
try:
    with open('previous_contents.json', 'r') as f:
        previous_contents = json.load(f)
    print("Loaded previous_contents.json", flush=True)
except FileNotFoundError:
    previous_contents = {url: None for url in URLS}
    print("Initialized previous_contents.json", flush=True)

changes = []
sent_reports = {time: False for time in REPORT_TIMES}
last_reset = datetime.now().date()
print("Variables initialized", flush=True)

def get_page_content(url):
    try:
        response = requests.get(url)
        print(f"Provjera {url}: Status {response.status_code}", flush=True)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text().strip()
    except Exception as e:
        print(f"Greška kod {url}: {str(e)}", flush=True)
        return f"Greška: {str(e)}"

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL
    msg['To'] = TO_EMAIL
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)
            print(f"E-mail poslan u {datetime.now().strftime('%H:%M')}", flush=True)
    except Exception as e:
        print(f"Greška pri slanju e-maila: {e}", flush=True)

print("Početak inicijalizacije...", flush=True)
for url in URLS:
    if previous_contents.get(url) is None:
        previous_contents[url] = get_page_content(url)
print("Inicijalizacija završena", flush=True)

print("Počinje praćenje...", flush=True)
while True:
    current_time = datetime.now()
    current_time_str = current_time.strftime("%H:%M")
    print(f"Provjera u {current_time_str} UTC", flush=True)

    if current_time.date() != last_reset:
        sent_reports = {time: False for time in REPORT_TIMES}
        last_reset = current_time.date()
        print("Resetiranje sent_reports za novi dan", flush=True)

    for url in URLS:
        current_content = get_page_content(url)
        if previous_contents[url] and current_content != previous_contents[url]:
            change_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
            changes.append(f"Promjena na {url} u {change_time}:\nStari sadržaj: {previous_contents[url][:200]}\nNovi sadržaj: {current_content[:200]}\n")
            previous_contents[url] = current_content
    print("Provjera URL-ova završena", flush=True)

    for report_time in REPORT_TIMES:
        report_hour, report_minute = map(int, report_time.split(":"))
        report_datetime = current_time.replace(hour=report_hour, minute=report_minute, second=0, microsecond=0)
        if current_time >= report_datetime and not sent_reports[report_time]:
            report = f"Dnevni sažetak promjena:\n\nBroj promjena: {len(changes)}\n\n" + ("\n".join(changes) if changes else "Nema promjena.")
            send_email(f"Dnevni izvještaj o promjenama ({report_time})", report)
            sent_reports[report_time] = True
            changes = []
    print("Slanje e-mailova završeno", flush=True)

    print("Spremam previous_contents.json...", flush=True)
    with open('previous_contents.json', 'w') as f:
        json.dump(previous_contents, f)
    print("Spremljeno previous_contents.json", flush=True)

    print(f"Čekam {CHECK_INTERVAL} sekundi...", flush=True)
    sys.stdout.flush()
    time.sleep(CHECK_INTERVAL)
