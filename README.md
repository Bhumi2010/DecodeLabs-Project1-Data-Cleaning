# Data Cleaning & Preparation — DecodeLabs Project 1

Industrial Training Kit Internship | Batch 2026 | DecodeLabs

## 📌 Objective
Clean a raw e-commerce dataset (1,200 records, 14 columns) by handling missing
values, duplicates, and inconsistent formatting — turning raw, messy data into
a reliable, production-ready source of truth.

## 🧹 What Was Done
- **Missing values**: Identified 309 blank `CouponCode` entries and imputed them as `"No Coupon"`
- **Duplicates**: Audited for duplicate rows and duplicate `OrderID`s — 0 found
- **Date formatting**: Standardized all dates to ISO 8601 (`YYYY-MM-DD`)
- **Text formatting**: Trimmed whitespace, applied consistent Proper Case to
  categorical fields (`Product`, `PaymentMethod`, `OrderStatus`, `ReferralSource`),
  uppercased ID fields
- **Numeric precision**: Enforced 2-decimal precision on `UnitPrice` and `TotalPrice`
- **Logical consistency check**: Verified `TotalPrice = Quantity × UnitPrice` across all records

## ✅ Verification Gate (Project 2 Threshold)
- 0% error rate on unique identifiers (no duplicate Order IDs)
- 0% error rate on date formats
- **Result: PASSED**

## 📂 Files in this Repo
| File | Description |
|---|---|
| `clean_data.py` | Python (pandas) script that performs the full cleaning workflow |
| `Cleaned_Data_Analytics.xlsx` | Final cleaned dataset |
| `Project1_Data_Cleaning_ChangeLog.pdf` | Documented change log of every cleaning step, rationale, and impact |

## 🛠 Tech Used
Python, pandas, openpyxl

## 👤 Author
**Bhumi Singh**
B.Tech CSE, AKTU
[GitHub](https://github.com/Bhumi2010) | [LinkedIn](https://linkedin.com/in/bhumi-singh-818b18334)
