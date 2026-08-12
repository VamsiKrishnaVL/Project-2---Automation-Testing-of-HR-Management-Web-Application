# OrangeHRM Demo Automation

## Project Overview
Automated functional testing for the OrangeHRM demo site: https://opensource-demo.orangehrmlive.com  
Framework: **Selenium + PyTest** using the **Page Object Model (POM)**. Tests cover login (data-driven), UI checks, user management, leave assignment, and claim submission.

## Repository Structure

orangehrm_automation/
├── pages/
├── tests/
├── utils/
├── testdata/
├── reports/
│   ├── screenshots/
│   └── logs/
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md


## Prerequisites
- Python 3.8+  
- Browser drivers in PATH (ChromeDriver, GeckoDriver, EdgeDriver)  
- Virtual environment recommended

## Install
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
pip install -r requirements.txt


Test Coverage
Implemented test cases (TC01–TC10):

TC01 — Data‑driven login using CSV/Excel; validate success/failure and logout after success.

TC02 — Home URL accessibility.

TC03 — Presence and enablement of username and password fields.

TC04 — Visibility and clickability of main menu items: Admin, PIM, Leave, Time, Recruitment, My Info, Performance, Dashboard.

TC05 — Create a new user via Admin → Add User; logout and validate new user login.

TC06 — Search and validate the newly created user in Admin → User Management.

TC07 — Verify “Forgot your password?” flow and confirmation message.

TC08 — Validate sub‑menu items under My Info (Personal Details, Contact Details, Emergency Contacts, Dependents).

TC09 — Assign leave to an employee and verify success message and record.

TC10 — Initiate a claim request (if module present) and verify submission; gracefully xfail if module not available.

Prerequisites
Python 3.8+

Browser drivers in PATH (ChromeDriver for Chrome, GeckoDriver for Firefox, EdgeDriver for Edge)

Virtual environment recommended