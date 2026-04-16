# CFMMC Settlement Downloader

An automation tool built with Playwright to log in to the China Futures Market Monitoring Center (CFMMC) Investor Service system and download daily settlement statements in batch (single date / date range / default trading day).

> The current repository folder name is `cffmc`, and all examples below use this path.

## ✨ Features

- Automatically logs in and downloads settlement reports by trading day
- Supports single-date download: `--date`
- Supports date-range download: `--start` + `--end`
- If no date is provided, resolves a default trading day automatically (today if trading day, otherwise previous trading day)
- Built-in local trading calendar filter (weekends + exchange holidays)
- Multi-account configuration via environment variables
- Organizes downloaded files as `downloads/account/date/`
- Can be scheduled via Windows Task Scheduler for daily automation

## 📁 Project Structure

```text
cffmc/
├── trading_calendar/
│   ├── calendar.py
│   └── holidays/
│       ├── shfe_2025.json
│       └── shfe_2026.json
├── downloads/
├── config.py
├── date_utils.py
├── downloader.py
├── main.py
├── run_daily.py
├── requirements.txt
└── README.md
```

## 🧰 Requirements

- Python 3.10+
- Windows (recommended; Task Scheduler friendly)
- Network access to the CFMMC login page

## 🚀 Quick Start

### 1) Install dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

### 2) Configure environment variables

Create a `.env` file in the project root (or configure system environment variables manually):

```env
CFMMC_USER_ACC1=your_username
CFMMC_PASS_ACC1=your_password
CFMMC_USER_ACC2=your_username_2
CFMMC_PASS_ACC2=your_password_2
```

Environment variable names must match the account configuration in `config.py`.

### 3) Run downloads

```bash
# Default mode: download for the default trading day
python main.py

# Download for a specific day
python main.py --date 2026-04-15

# Download for a date range
python main.py --start 2026-04-10 --end 2026-04-14

# Specify account key (example)
python main.py --account acc1
```

### 4) Daily scheduled run

```bash
python run_daily.py
```

This script automatically resolves the default trading day and performs a one-day download.

## ⏰ Windows Task Scheduler (Example)

| Item | Example Value |
|---|---|
| Program/script | `C:\Path\To\python.exe` |
| Add arguments | `run_daily.py` |
| Start in | `D:\CodeProjects\cffmc` |

Recommended trigger time: after market close on trading days (e.g. 19:00).

## 🗓️ Trading Calendar

Holiday files are stored in: `trading_calendar/holidays/`.

- `shfe_2025.json`
- `shfe_2026.json`

Update yearly holiday files based on official exchange announcements.

## 🔐 Security Notes

- `.env`, `downloads/`, `logs/`, `__pycache__/`, etc. are excluded via `.gitignore`.
- Never commit real account credentials.

## ⚠️ Disclaimer

This project is for learning and automation practice. You are responsible for ensuring your usage complies with CFMMC terms and applicable laws/regulations.

## 📄 License

MIT License (see the repository license file).