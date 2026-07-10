# ============================================================
# Data Quality Check
# Purpose:
#   Perform basic validation on the Bronze table before
#   transforming data into the Silver layer.
# ============================================================

# ------------------------------------------------------------
# Total number of records
# ------------------------------------------------------------
bronze.count()

# ------------------------------------------------------------
# Verify available columns
# ------------------------------------------------------------
bronze.columns

# ------------------------------------------------------------
# Inspect data types
# ------------------------------------------------------------
bronze.printSchema()

# ------------------------------------------------------------
# Summary statistics for numeric columns
# Useful for detecting unexpected values
# ------------------------------------------------------------
bronze.describe().show()

# ------------------------------------------------------------
# Validate row count using SQL expression
# ------------------------------------------------------------
bronze.selectExpr(
    "count(*) as total_rows"
).show()