# 🏦 Bank Reconciliation Engine

> A fintech-grade reconciliation dashboard that compares internal transaction records with bank statements to detect mismatches, missing entries, duplicates, and anomalies.

---

## 📌 Project Overview

The **Bank Reconciliation Engine** is a data-driven application designed to simulate real-world financial reconciliation workflows used by banks, fintech companies, and payment processors.

It enables users to upload two transaction datasets:
- Internal system records
- Bank statement records

The system automatically compares them and generates:
- Reconciliation results
- Exception reports
- Visual analytics dashboard


## 🌐 Live Demo

👉 https://sourabhsyy-bank-reconciliation-engine-app-fxmqdc.streamlit.app


---

## 🎯 Key Features

### 🔄 Reconciliation Engine
- Matches transactions across datasets
- Supports flexible column mapping (transaction_id or custom keys)
- Handles real-world inconsistencies

### 🚨 Exception Detection
- ✅ Matched Transactions  
- ❌ Missing in Bank  
- ❌ Missing in Internal  
- ⚠️ Amount Mismatch  
- ⚠️ Status Mismatch  
- 🔁 Duplicate Transactions  

### 📊 Analytics Dashboard
- Summary metrics (counts of each category)
- Pie chart for distribution
- Bar chart for comparison
- Interactive UI

### 📁 File Handling
- Upload CSV files dynamically
- Auto-detect column names
- Handles different naming formats

### 📥 Export
- Download reconciliation report as CSV

---

## 🖥️ Application Screenshots

### 🔹 Dashboard Overview
<img width="1366" height="648" alt="image" src="https://github.com/user-attachments/assets/874d1368-4a2d-4e8e-adac-4f25f5706338" />


### 🔹 Reconciliation Results
<img width="1366" height="625" alt="image" src="https://github.com/user-attachments/assets/a03e3e56-425b-410b-b5ce-962b28a3ec69" />


### 🔹 Analytics Charts
<img width="1366" height="598" alt="image" src="https://github.com/user-attachments/assets/7f2ed3d8-6170-40f1-9701-f8d41311d8a5" />


---

## 🧠 How It Works

1. Upload internal transaction CSV
2. Upload bank statement CSV
3. System normalizes column names
4. User selects matching columns (if needed)
5. Duplicate records are detected separately
6. Clean datasets are merged
7. Transactions are classified into categories
8. Results displayed via:
   - Tables
   - Metrics
   - Charts
9. Final report available for download

---

## 🧾 Reconciliation Categories

| Category | Description |
|--------|------------|
| ✅ Matched | Present in both datasets with same values |
| ❌ Missing in Bank | Present only in internal records |
| ❌ Missing in Internal | Present only in bank records |
| ⚠️ Amount Mismatch | Same transaction but different amount |
| ⚠️ Status Mismatch | Same transaction but different status |
| 🔁 Duplicates | Repeated transaction records |

---

## 🛠️ Tech Stack

- **Python**
- **Pandas**
- **Streamlit**
- **Plotly**

---

## 📂 Project Structure
bank-reconciliation-engine/
│
├── app.py
├── reconciliation.py
├── requirements.txt
├── README.md
├── sample_data/
│ ├── internal_transactions.csv
│ └── bank_transactions.csv
└── screenshots/


---

## ⚙️ Installation & Setup

```bash
# Install dependencies
python -m pip install -r requirements.txt

# Run the app
python -m streamlit run app.py
