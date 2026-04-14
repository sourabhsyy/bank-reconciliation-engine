import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Bank Reconciliation Engine", layout="wide")

st.title(" Bank Reconciliation Engine")
st.caption("Upload internal and bank transaction files to compare records and detect exceptions.")

internal_file = st.file_uploader("Upload Internal Transactions CSV", type=["csv"])
bank_file = st.file_uploader("Upload Bank Transactions CSV", type=["csv"])

COLUMN_ALIASES = {
    "transaction_id": ["transaction_id", "txn_id", "txnid", "txn", "id", "transactionid"],
    "date": ["date", "txn_date", "transaction_date", "payment_date"],
    "amount": ["amount", "amt", "transaction_amount", "payment_amount"],
    "status": ["status", "txn_status", "transaction_status", "payment_status"],
    "bank_status": ["bank_status", "status", "txn_status", "transaction_status"],
    "reference_number": ["reference_number", "reference", "ref_no", "ref_number", "rrn"]
}

def normalize_columns(df):
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    return df

def find_column(df, possible_names):
    for col in df.columns:
        if col in possible_names:
            return col
    return None

def rename_with_aliases(df, file_type="internal"):
    df = normalize_columns(df.copy())

    renamed = {}

    if file_type == "internal":
        txn_col = find_column(df, COLUMN_ALIASES["transaction_id"])
        date_col = find_column(df, COLUMN_ALIASES["date"])
        amount_col = find_column(df, COLUMN_ALIASES["amount"])
        status_col = find_column(df, COLUMN_ALIASES["status"])

        if txn_col:
            renamed[txn_col] = "transaction_id"
        if date_col:
            renamed[date_col] = "date"
        if amount_col:
            renamed[amount_col] = "amount"
        if status_col:
            renamed[status_col] = "status"

    elif file_type == "bank":
        txn_col = find_column(df, COLUMN_ALIASES["transaction_id"])
        date_col = find_column(df, COLUMN_ALIASES["date"])
        amount_col = find_column(df, COLUMN_ALIASES["amount"])
        bank_status_col = find_column(df, COLUMN_ALIASES["bank_status"])
        ref_col = find_column(df, COLUMN_ALIASES["reference_number"])

        if txn_col:
            renamed[txn_col] = "transaction_id"
        if date_col:
            renamed[date_col] = "date"
        if amount_col:
            renamed[amount_col] = "amount"
        if bank_status_col:
            renamed[bank_status_col] = "bank_status"
        if ref_col:
            renamed[ref_col] = "reference_number"

    return df.rename(columns=renamed)

if internal_file and bank_file:
    internal_df = pd.read_csv(internal_file)
    bank_df = pd.read_csv(bank_file)

    internal_df = rename_with_aliases(internal_df, "internal")
    bank_df = rename_with_aliases(bank_df, "bank")

    st.subheader("Detected Columns")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Internal File Columns**")
        st.write(list(internal_df.columns))

    with c2:
        st.markdown("**Bank File Columns**")
        st.write(list(bank_df.columns))

    common_match_options = list(set(internal_df.columns).intersection(set(bank_df.columns)))
    common_match_options = [col for col in common_match_options if col not in ["status", "bank_status", "reference_number"]]

    default_match = ["transaction_id"] if "transaction_id" in common_match_options else []

    st.subheader("Match Configuration")

    match_columns = st.multiselect(
        "Select columns to match records",
        options=common_match_options,
        default=default_match
    )

    if not match_columns:
        st.error("Please select at least one common column for matching.")
        st.stop()

    if "amount" not in internal_df.columns or "amount" not in bank_df.columns:
        st.error("Both files must contain an amount column (or a recognizable alias like amt / transaction_amount).")
        st.stop()

    internal_df["amount"] = pd.to_numeric(internal_df["amount"], errors="coerce")
    bank_df["amount"] = pd.to_numeric(bank_df["amount"], errors="coerce")

    st.subheader("Uploaded Data")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Internal Transactions**")
        st.dataframe(internal_df, use_container_width=True)

    with col2:
        st.markdown("**Bank Transactions**")
        st.dataframe(bank_df, use_container_width=True)

    internal_duplicates = internal_df[internal_df.duplicated(subset=match_columns, keep=False)]
    bank_duplicates = bank_df[bank_df.duplicated(subset=match_columns, keep=False)]

    internal_clean = internal_df.drop_duplicates(subset=match_columns, keep="first")
    bank_clean = bank_df.drop_duplicates(subset=match_columns, keep="first")

    merged_df = pd.merge(
        internal_clean,
        bank_clean,
        on=match_columns,
        how="outer",
        indicator=True,
        suffixes=("_internal", "_bank")
    )

    def get_status(row):
        if row["_merge"] == "both":
            if row.get("amount_internal") != row.get("amount_bank"):
                return "Amount Mismatch"

            if "status" in merged_df.columns and "bank_status" in merged_df.columns:
                internal_status = str(row.get("status", "")).lower()
                bank_status = str(row.get("bank_status", "")).lower()
                if internal_status and bank_status and internal_status != bank_status:
                    return "Status Mismatch"

            return "Matched"

        elif row["_merge"] == "left_only":
            return "Missing in Bank"

        elif row["_merge"] == "right_only":
            return "Missing in Internal"

    merged_df["reconciliation_status"] = merged_df.apply(get_status, axis=1)

    matched_count = int((merged_df["reconciliation_status"] == "Matched").sum())
    amount_mismatch_count = int((merged_df["reconciliation_status"] == "Amount Mismatch").sum())
    missing_bank_count = int((merged_df["reconciliation_status"] == "Missing in Bank").sum())
    missing_internal_count = int((merged_df["reconciliation_status"] == "Missing in Internal").sum())
    status_mismatch_count = int((merged_df["reconciliation_status"] == "Status Mismatch").sum())
    internal_duplicate_count = len(internal_duplicates)
    bank_duplicate_count = len(bank_duplicates)

    st.subheader("Summary Metrics")

    m1, m2, m3, m4, m5, m6, m7 = st.columns(7)
    m1.metric("Matched", matched_count)
    m2.metric("Amount Mismatch", amount_mismatch_count)
    m3.metric("Missing in Bank", missing_bank_count)
    m4.metric("Missing in Internal", missing_internal_count)
    m5.metric("Status Mismatch", status_mismatch_count)
    m6.metric("Internal Duplicates", internal_duplicate_count)
    m7.metric("Bank Duplicates", bank_duplicate_count)

    summary = merged_df["reconciliation_status"].value_counts().reset_index()
    summary.columns = ["Status", "Count"]

    st.subheader("Analytics")

    c1, c2 = st.columns(2)

    with c1:
        pie_fig = px.pie(
            summary,
            names="Status",
            values="Count",
            title="Reconciliation Status Distribution"
        )
        st.plotly_chart(pie_fig, use_container_width=True)

    with c2:
        bar_fig = px.bar(
            summary,
            x="Status",
            y="Count",
            title="Reconciliation Status Counts"
        )
        st.plotly_chart(bar_fig, use_container_width=True)

    st.subheader("Reconciliation Result")
    st.dataframe(merged_df, use_container_width=True)

    matched_df = merged_df[merged_df["reconciliation_status"] == "Matched"]
    amount_mismatch_df = merged_df[merged_df["reconciliation_status"] == "Amount Mismatch"]
    missing_bank_df = merged_df[merged_df["reconciliation_status"] == "Missing in Bank"]
    missing_internal_df = merged_df[merged_df["reconciliation_status"] == "Missing in Internal"]
    status_mismatch_df = merged_df[merged_df["reconciliation_status"] == "Status Mismatch"]

    st.subheader("Exception Views")

    with st.expander(" Matched Transactions"):
        st.dataframe(matched_df, use_container_width=True)

    with st.expander(" Amount Mismatch"):
        st.dataframe(amount_mismatch_df, use_container_width=True)

    with st.expander(" Missing in Bank"):
        st.dataframe(missing_bank_df, use_container_width=True)

    with st.expander(" Missing in Internal"):
        st.dataframe(missing_internal_df, use_container_width=True)

    with st.expander(" Status Mismatch"):
        st.dataframe(status_mismatch_df, use_container_width=True)

    with st.expander(" Duplicates in Internal"):
        st.dataframe(internal_duplicates, use_container_width=True)

    with st.expander(" Duplicates in Bank"):
        st.dataframe(bank_duplicates, use_container_width=True)

    csv = merged_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Reconciliation Report",
        data=csv,
        file_name="reconciliation_report.csv",
        mime="text/csv"
    )