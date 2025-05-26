# RERA Odisha Project Scraper

A Playwright-based Python script that scrapes real estate project details from the official [RERA Odisha website](https://rera.odisha.gov.in/projects/project-list). Extracts project name, registration number, promoter company details, and GST number.

## What It Does

- Navigates the project listing page.
- Opens individual project detail pages.
- Extracts:
  - Project Name
  - RERA Registration Number
  - Promoter Company Name
  - Promoter Office Address
  - GST Number

## How It Works

- Uses *Playwright (sync API)* for browser automation.
- Opens each project detail in sequence.
- Waits for loaders and dynamic content to load.
- Handles errors and incomplete data gracefully.
- Collects and prints data for the first 6 projects (customizable).

## How to Run

### 1. Install Playwright and Dependencies

pip install playwright
python -m playwright install

### 2. Run the Script

python scrape_rera.py

## Sample Output

📄 Project 1
RERA Regd. No: MP/19/2024/00548
Project Name: Green Valley Heights
Promoter Name: Triveni Buildtech Pvt Ltd
Promoter Address: Plot No. 78, Saheed Nagar, Bhubaneswar
GST No: 21AAACT1234B1Z5

📄 Project 2
RERA Regd. No: MP/05/2024/00112
Project Name: Golden Nest Phase 2
Promoter Name: Golden Infra Pvt Ltd
Promoter Address: 12A, Janpath, Bhubaneswar
GST No: 21AABCG5678M1ZQ
