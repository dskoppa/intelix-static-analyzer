# 🔬 SophosLabs Intelix Static File Analyzer

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-Active-brightgreen.svg)]()

Submit `.exe`, `.docx`, and `.pdf` files for **static analysis** using the [SophosLabs Intelix API](https://www.sophos.com/en-us/intelix). This tool handles file submission, polling, and saves JSON reports as `.txt` with real-time logs.

---

## 📦 Features

- ✅ OAuth2 Token Authentication
- 📤 Upload multiple files
- ⏳ Poll for analysis job results
- 📄 Save structured JSON reports (`.txt`)
- 📝 Auto-logging to console and log files
- 💬 Easy configuration via `.env`

---

## 🧱 Project Structure

```bash
.
├── sample_files/            # Input files (.exe, .docx, .pdf)
├── reports/                 # Output reports (.txt)
├── logs/                    # Log files
├── config.env               # Environment variables (API credentials)
├── intelix_static_analysis.py
├── requirements.txt
└── README.md
````

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/dskoppa/intelix-static-analyzer.git
cd intelix-static-analyzer
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Credentials

Create a `.env` file or `config.env`:

```env
CLIENT_ID=your_client_id_here
CLIENT_SECRET=your_client_secret_here
```

> ⚠️ Never commit this file. It's ignored via `.gitignore`.

### 4. Add Files to Analyze

Drop your `.exe`, `.docx`, and `.pdf` files into the `sample_files/` directory.

### 5. Run the Script

```bash
python intelix_static_analysis.py
```

---

## 📂 Output

* 📁 `reports/` — `.txt` reports (e.g., `sample.docx.txt`)
* 📁 `logs/` — timestamped `.log` file with full trace
* 🖥 Console log — live status of submissions and polling

---

## 🧪 Sample Log Output

```
🔍 Starting SophosLabs Intelix static file analysis...
🔐 Requesting OAuth access token...
✅ Access token successfully retrieved.
📤 Submitting file: malware.exe
⏳ Waiting for report for job: 1234abcd5678...
📄 Report saved: reports/malware.exe.txt
✅ All file submissions and reports complete.
```

---

## 🛡️ API & Region

* API: [Intelix Static File Analysis API v1](https://developer.sophos.com/docs/intelix/v1/overview)
* Endpoint used: `https://de.api.labs.sophos.com`

---

## 📄 License

MIT © 2025
This is a demo tool. Use at your own discretion with non-sensitive files.

---

## ✨ Contribution

Pull requests welcome!
Feel free to fork, raise issues, and improve.

---

## 📬 Contact

**Developer:** Dinesh
📧 \[[dskoppa@gmail.com](mailto:dskoppa@gmail.com)]

