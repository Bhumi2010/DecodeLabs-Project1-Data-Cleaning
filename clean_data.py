"""
DecodeLabs Internship - Project 1: Data Cleaning & Preparation
Author: Bhumi Singh
Dataset: Dataset_for_Data_Analytics.xlsx
"""

import pandas as pd

INPUT_PATH = "/mnt/user-data/uploads/Dataset_for_Data_Analytics.xlsx"
OUTPUT_PATH = "/mnt/user-data/outputs/Cleaned_Data_Analytics.xlsx"

change_log = []

def log(change_id, description, impact, status="Resolved"):
    change_log.append({
        "Change ID": change_id,
        "Description": description,
        "Impact": impact,
        "Status": status
    })

# ---------------------------------------------------------
# 1. LOAD DATA
# ---------------------------------------------------------
df = pd.read_excel(INPUT_PATH)
original_shape = df.shape
log("CR000", f"Loaded raw dataset ({original_shape[0]} rows x {original_shape[1]} cols)",
    "Baseline established", "Resolved")

# ---------------------------------------------------------
# 2. IDENTIFY MISSING / NULL VALUES
# ---------------------------------------------------------
null_counts = df.isnull().sum()
missing_cols = null_counts[null_counts > 0]

if not missing_cols.empty:
    for col, cnt in missing_cols.items():
        if col == "CouponCode":
            df[col] = df[col].fillna("No Coupon")
            log("CR001", f"Imputed '{col}' missing values with 'No Coupon'",
                f"Resolved {cnt} missing records (no promo applied at checkout)")
        else:
            # Generic fallback strategy: numeric -> median, text -> mode
            if pd.api.types.is_numeric_dtype(df[col]):
                fill_val = df[col].median()
                df[col] = df[col].fillna(fill_val)
                log("CR00X", f"Imputed '{col}' missing values using Median ({fill_val})",
                    f"Preserved {cnt} records")
            else:
                fill_val = df[col].mode().iloc[0]
                df[col] = df[col].fillna(fill_val)
                log("CR00X", f"Imputed '{col}' missing values using Mode ('{fill_val}')",
                    f"Preserved {cnt} records")
else:
    log("CR001", "Audit found 0 missing/null values across all 14 columns",
        "No imputation required - dataset already null-clean")

# ---------------------------------------------------------
# 3. REMOVE DUPLICATES
# ---------------------------------------------------------
full_dupes = df.duplicated().sum()
id_dupes = df.duplicated(subset=["OrderID"]).sum()

before = len(df)
df = df.drop_duplicates()
df = df.drop_duplicates(subset=["OrderID"], keep="first")
after = len(df)

if full_dupes or id_dupes:
    log("CR002", f"Removed {full_dupes} full-row duplicates and {id_dupes} duplicate OrderIDs",
        f"Row count reduced from {before} to {after}")
else:
    log("CR002", "Audit confirmed 0 duplicate rows and 0 duplicate OrderIDs",
        "Verification Gate (0% error rate on unique identifiers) PASSED")

# ---------------------------------------------------------
# 4. CORRECT DATA FORMATS
# ---------------------------------------------------------

# 4a. Dates -> ISO 8601 (YYYY-MM-DD)
df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.strftime("%Y-%m-%d")
bad_dates = df["Date"].isnull().sum()
log("CR003", "Standardized 'Date' column to ISO 8601 format (YYYY-MM-DD)",
    f"{bad_dates} unparseable dates found" if bad_dates else "Verification Gate (0% error rate on date formats) PASSED")

# 4b. Text columns -> trim whitespace + consistent case
text_cols = ["OrderID", "CustomerID", "Product", "ShippingAddress",
             "PaymentMethod", "OrderStatus", "TrackingNumber",
             "CouponCode", "ReferralSource"]
trim_count = 0
for col in text_cols:
    stripped = df[col].astype(str).str.strip()
    trim_count += (stripped != df[col].astype(str)).sum()
    df[col] = stripped

log("CR004", "Trimmed leading/trailing whitespace across all text columns",
    f"{trim_count} cell values normalized")

# Proper-case categorical/free-text columns where appropriate
df["Product"] = df["Product"].str.title()
df["PaymentMethod"] = df["PaymentMethod"].str.title()
df["OrderStatus"] = df["OrderStatus"].str.title()
df["ReferralSource"] = df["ReferralSource"].str.title()
log("CR005", "Applied consistent Proper Case to categorical text fields "
              "(Product, PaymentMethod, OrderStatus, ReferralSource)",
    "Eliminated case-sensitivity inconsistencies (e.g., 'mumbai' vs 'MUMBAI' style issues)")

# IDs upper-cased for consistency
df["OrderID"] = df["OrderID"].str.upper()
df["CustomerID"] = df["CustomerID"].str.upper()
df["TrackingNumber"] = df["TrackingNumber"].str.upper()

# 4c. Numeric precision -> 2 decimals
for col in ["UnitPrice", "TotalPrice"]:
    df[col] = df[col].astype(float).round(2)
log("CR006", "Enforced 2-decimal numeric precision on 'UnitPrice' and 'TotalPrice'",
    "Standardized currency precision across all records")

# 4d. Integer columns -> ensure proper int type
for col in ["Quantity", "ItemsInCart"]:
    df[col] = df[col].astype(int)

# ---------------------------------------------------------
# 5. LOGICAL CONSISTENCY CHECK (TotalPrice = Quantity x UnitPrice)
# ---------------------------------------------------------
calc_total = (df["Quantity"] * df["UnitPrice"]).round(2)
mismatches = (calc_total != df["TotalPrice"]).sum()
if mismatches:
    df["TotalPrice"] = calc_total
    log("CR007", f"Recalculated 'TotalPrice' for {mismatches} rows where it did not equal Quantity x UnitPrice",
        f"Corrected {mismatches} pricing inconsistencies")
else:
    log("CR007", "Audit confirmed TotalPrice = Quantity x UnitPrice for all rows",
        "No pricing inconsistencies found")

# ---------------------------------------------------------
# 6. FINAL VERIFICATION GATE (Project 1 -> Project 2 threshold)
# ---------------------------------------------------------
final_dupe_ids = df.duplicated(subset=["OrderID"]).sum()
final_bad_dates = df["Date"].isnull().sum()

gate_passed = (final_dupe_ids == 0) and (final_bad_dates == 0)
log("CR008", "Final verification gate check executed",
    f"Duplicate IDs: {final_dupe_ids} | Bad date formats: {final_bad_dates} | "
    f"Gate {'PASSED ✅' if gate_passed else 'FAILED ❌'}")

# ---------------------------------------------------------
# 7. SAVE CLEANED OUTPUT
# ---------------------------------------------------------
df.to_excel(OUTPUT_PATH, index=False)

print(f"Original shape: {original_shape}")
print(f"Final shape:   {df.shape}")
print(f"Gate passed:   {gate_passed}")
print(f"Saved to: {OUTPUT_PATH}")

import json
with open("/home/claude/work/change_log.json", "w") as f:
    json.dump(change_log, f, indent=2)
