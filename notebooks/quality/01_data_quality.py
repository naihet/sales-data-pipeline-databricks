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

# ------------------------------------------------------------
# Check missing values
# ------------------------------------------------------------
bronze.select([
    F.count(F.when(F.col(c).isNull(), c)).alias(c)
    for c in bronze.columns
]).show()

# ------------------------------------------------------------
# Check duplicate Order ID
# ------------------------------------------------------------
bronze.groupBy("order_id") \
      .count() \
      .filter("count > 1") \
      .show()
      
# ------------------------------------------------------------
# Verify row count before and after transformation
# ------------------------------------------------------------
print(f"Total Rows: {bronze.count()}")