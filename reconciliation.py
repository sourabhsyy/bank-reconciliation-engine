import pandas as pd

# Load data
internal_df = pd.read_csv("sample_data/internal_transactions.csv")
bank_df = pd.read_csv("sample_data/bank_transactions.csv")

# Merge both datasets on transaction_id
merged_df = pd.merge(
    internal_df,
    bank_df,
    on="transaction_id",
    how="outer",
    indicator=True
)

# Create reconciliation status column
def get_status(row):
    if row["_merge"] == "both":
        if row["amount_x"] == row["amount_y"]:
            return "Matched"
        else:
            return "Amount Mismatch"
    elif row["_merge"] == "left_only":
        return "Missing in Bank"
    elif row["_merge"] == "right_only":
        return "Missing in Internal"

merged_df["reconciliation_status"] = merged_df.apply(get_status, axis=1)

# Print results
print("\n=== FULL RECONCILIATION RESULT ===")
print(merged_df[["transaction_id", "amount_x", "amount_y", "_merge", "reconciliation_status"]])

# Summary counts
print("\n=== SUMMARY ===")
print(merged_df["reconciliation_status"].value_counts())

# Detect duplicates in internal data
internal_duplicates = internal_df[internal_df.duplicated(subset=["transaction_id"], keep=False)]

print("\n=== DUPLICATES IN INTERNAL SYSTEM ===")
print(internal_duplicates)

def check_status_mismatch(row):
    if row["_merge"] == "both":
        if str(row["status"]).lower() != str(row["bank_status"]).lower():
            return True
    return False

merged_df["status_mismatch"] = merged_df.apply(check_status_mismatch, axis=1)

print("\n=== STATUS MISMATCH ===")
print(merged_df[merged_df["status_mismatch"] == True][["transaction_id", "status", "bank_status"]])

