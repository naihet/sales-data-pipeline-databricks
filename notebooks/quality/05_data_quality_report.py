# Databricks notebook source
# ============================================================
# Data Quality Report
# Purpose:
#   - Validate data quality across Bronze and Silver layers.
#   - Check row counts, missing values, duplicate records,
#     invalid values, and schema consistency.
#   - Generate a summary report for pipeline validation.
# ============================================================

from pyspark.sql.functions import col, when, sum

# ------------------------------------------------------------
# Read Bronze and Silver tables
# ------------------------------------------------------------

bronze = spark.read.table("workspace.salesdb.bronze_sales")
silver = spark.read.table("workspace.salesdb.silver_sales")

# ------------------------------------------------------------
# Row Count Validation
# Compare total records between Bronze and Silver
# ------------------------------------------------------------

bronze_count = bronze.count()
silver_count = silver.count()

print(f"Bronze Rows : {bronze_count}")
print(f"Silver Rows : {silver_count}")

# ------------------------------------------------------------
# Schema Validation
# ------------------------------------------------------------

print("Bronze Schema")
bronze.printSchema()

print("Silver Schema")
silver.printSchema()

# ------------------------------------------------------------
# Missing Value Report
# ------------------------------------------------------------

silver.select([
    sum(
        when(col(c).isNull(), 1).otherwise(0)
    ).alias(c)
    for c in silver.columns
]).show()

# ------------------------------------------------------------
# Duplicate Record Validation
# ------------------------------------------------------------

duplicate_count = silver.count() - silver.dropDuplicates().count()

print(f"Duplicate Records : {duplicate_count}")

# ------------------------------------------------------------
# Business Rule Validation
# ------------------------------------------------------------

negative_sales = silver.filter(
    col("sales") < 0
).count()

print(f"Negative Sales : {negative_sales}")

invalid_quantity = silver.filter(
    col("quantity") <= 0
).count()

print(f"Invalid Quantity : {invalid_quantity}")

invalid_discount = silver.filter(
    (col("discount") < 0) |
    (col("discount") > 1)
).count()

print(f"Invalid Discount : {invalid_discount}")

profit_null = silver.filter(
    col("profit").isNull()
).count()

print(f"NULL Profit : {profit_null}")

# ------------------------------------------------------------
# Data Quality Summary
# ------------------------------------------------------------

print("=" * 50)
print("DATA QUALITY REPORT")
print("=" * 50)

print(f"Bronze Rows        : {bronze_count}")
print(f"Silver Rows        : {silver_count}")
print(f"Duplicate Records  : {duplicate_count}")
print(f"Negative Sales     : {negative_sales}")
print(f"Invalid Quantity   : {invalid_quantity}")
print(f"Invalid Discount   : {invalid_discount}")
print(f"NULL Profit        : {profit_null}")

# ------------------------------------------------------------
# Dataset Statistics
# ------------------------------------------------------------

silver.describe(
    "sales",
    "quantity",
    "discount",
    "profit"
).show()

# ------------------------------------------------------------
# Preview Silver Dataset
# ------------------------------------------------------------

display(silver.limit(20))