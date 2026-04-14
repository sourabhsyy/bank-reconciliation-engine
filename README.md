# Bank Reconciliation Engine

A fintech-focused reconciliation dashboard that compares internal transaction records with bank statement records to identify matched transactions, missing records, amount mismatches, status mismatches, and duplicate entries.

## Overview

This project simulates a real-world reconciliation workflow used in payment systems and financial operations. It helps identify transaction exceptions by comparing two uploaded transaction datasets and generating a reconciliation report with summary metrics and analytics.

## Features

- Upload internal and bank transaction CSV files
- Auto-normalize common column names
- Compare transactions using selected matching columns
- Detect:
  - Matched transactions
  - Missing in Bank
  - Missing in Internal
  - Amount Mismatch
  - Status Mismatch
  - Duplicate transactions
- View summary metrics
- Visualize reconciliation status with charts
- Download reconciliation report as CSV

## Tech Stack

- Python
- Pandas
- Streamlit
- Plotly

## Project Structure

```bash
bank-reconciliation-engine/
│
├── app.py
├── reconciliation.py
├── requirements.txt
├── README.md
└── sample_data/
    ├── internal_transactions.csv
    └── bank_transactions.csv


    