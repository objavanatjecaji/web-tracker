import requests
from bs4 import BeautifulSoup
import time
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from datetime import timedelta  # Dodan ovaj import
import json

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
REPORT_TIMES = ["12:05", "14:05", "18:05", "21:05"]  # CEST times

print("Starting script...")
try:
    print("Trying to load previous_contents.json...")
    with open('previous_contents.json', 'r') as f:
        previous_contents = json.load(f)
    print("Loaded previous_contents.json successfully")
except FileNotFoundError:
    print("previous_contents.json not found, initializing...")
    previous_contents = {url: None for url in URLS}
except Exception as e:
    print(f"Error loading previous_contents.json: {str(e)}")
    previous_contents = {url: None for url in URLS}

changes = []
sent_reports = {time: False for time in REPORT_TIMES}
last_reset = datetime.now().date()

def get_page_content(url):
    try:
        print(f"Fetching {url}...")
        response = requests.get(url, timeout=10)
        print(f"Provjera {url}: Status {response.status_code}")
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text().strip()
    except Exception as e:
        print(f"Greška kod {url}: {str(e)}")
        return f"Greška: {str(e)}"

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL
    msg
