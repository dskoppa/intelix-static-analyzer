import os
import time
import json
import logging
import requests
from datetime import datetime
from dotenv import load_dotenv

# === Configuration ===
load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

AUTH_URL = "https://api.labs.sophos.com/oauth2/token"
ANALYSIS_URL = "https://de.api.labs.sophos.com/analysis/file/static/v1/"
REPORT_URL_TEMPLATE = "https://de.api.labs.sophos.com/analysis/file/static/v1/reports/{}?report_format=json"

SAMPLE_DIR = "./sample_files"
REPORT_DIR = "./reports"
LOG_DIR = "./logs"
POLL_INTERVAL = 5  # seconds
TIMEOUT = 15 * 60  # 15 minutes

# === Logging Setup ===
os.makedirs(LOG_DIR, exist_ok=True)
log_file = os.path.join(LOG_DIR, f"intelix_static_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logging.getLogger().addHandler(console)

# === Auth Token ===
def get_access_token():
    logging.info("🔐 Requesting OAuth access token...")
    response = requests.post(
        AUTH_URL,
        data={"grant_type": "client_credentials"},
        auth=(CLIENT_ID, CLIENT_SECRET),
    )
    response.raise_for_status()
    token = response.json().get("access_token")
    logging.info("✅ Access token successfully retrieved.")
    return token

# === Submit File ===
def submit_file(file_path, token):
    with open(file_path, "rb") as f:
        files = {"file": (os.path.basename(file_path), f)}
        headers = {"Authorization": f"Bearer {token}"}
        logging.info(f"📤 Submitting file: {os.path.basename(file_path)}")
        response = requests.post(ANALYSIS_URL, headers=headers, files=files)
        if response.status_code not in [200, 202]:
            logging.error(f"❌ Submission failed for {file_path}: {response.status_code} - {response.text}")
            return None
        job_id = response.json().get("jobId")
        return job_id

# === Poll for Report ===
def fetch_report(job_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    url = REPORT_URL_TEMPLATE.format(job_id)
    start = time.time()

    while time.time() - start < TIMEOUT:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("jobStatus") == "SUCCESS":
                return data
            elif data.get("jobStatus") == "ERROR":
                logging.error(f"❌ Job failed: {data}")
                return None
        elif response.status_code == 404:
            logging.info(f"ℹ️ Report not ready yet for job: {job_id}")
        else:
            logging.warning(f"⚠️ Unexpected status for job {job_id}: {response.status_code} - {response.text}")
        time.sleep(POLL_INTERVAL)

    logging.error(f"⏱️ Timeout waiting for report on job {job_id}")
    return None

# === Save Report ===
def save_report(report_data, file_path):
    os.makedirs(REPORT_DIR, exist_ok=True)
    base_name = os.path.basename(file_path)
    report_path = os.path.join(REPORT_DIR, f"{base_name}.txt")

    with open(report_path, "w") as f:
        f.write(json.dumps(report_data, indent=2))
    logging.info(f"📄 Report saved: {report_path}")

# === Main ===
def main():
    logging.info("🔍 Starting SophosLabs Intelix static file analysis...")
    token = get_access_token()
    if not token:
        logging.error("❌ Failed to get token. Exiting.")
        return

    if not os.path.isdir(SAMPLE_DIR):
        logging.error(f"❌ Sample directory '{SAMPLE_DIR}' not found.")
        return

    files = [f for f in os.listdir(SAMPLE_DIR) if os.path.isfile(os.path.join(SAMPLE_DIR, f))]
    if not files:
        logging.warning("⚠️ No files found in sample_files/ directory.")
        return

    for file_name in files:
        file_path = os.path.join(SAMPLE_DIR, file_name)
        job_id = submit_file(file_path, token)
        if not job_id:
            continue
        logging.info(f"⏳ Waiting for report for job: {job_id}")
        report = fetch_report(job_id, token)
        if report:
            save_report(report, file_path)
        else:
            logging.error(f"❌ No report generated for file: {file_name}")

    logging.info("✅ All file submissions and reports complete.")

if __name__ == "__main__":
    main()
