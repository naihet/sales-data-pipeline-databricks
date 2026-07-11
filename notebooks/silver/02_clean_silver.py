# Databricks notebook source
# DBTITLE 1,02_clean_silver
# ============================================================
# Silver Layer
# Purpose:
#   - Read data from the Bronze layer.
#   - Clean and validate the dataset.
#   - Convert data types for downstream processing.
#   - Remove duplicate records.
#   - Store cleaned data in the Silver layer.
# ============================================================

from pyspark.sql.functions import col, sum, when

# ------------------------------------------------------------
# Read data from Bronze layer
# ------------------------------------------------------------
bronze = spark.read.table("workspace.salesdb.bronze_sales")

# ------------------------------------------------------------
# Convert data types
# ------------------------------------------------------------
silver = (
    bronze
    .withColumn("sales", col("sales").cast("double"))
    .withColumn("quantity", col("quantity").cast("int"))
    .withColumn("discount", col("discount").cast("double"))
)

# ------------------------------------------------------------
# Inspect schema after type conversion
# ------------------------------------------------------------
silver.printSchema()

# ------------------------------------------------------------
# Data Quality Check
# Count missing (NULL) values in each column
# ------------------------------------------------------------
silver.select([
    sum(when(col(c).isNull(), 1).otherwise(0)).alias(c)
    for c in silver.columns
]).show()

# ------------------------------------------------------------
# Remove duplicate records
# ------------------------------------------------------------
before_count = silver.count()

silver = silver.dropDuplicates()

after_count = silver.count()

print(f"Rows before removing duplicates : {before_count}")
print(f"Rows after removing duplicates  : {after_count}")

# ------------------------------------------------------------
# Business Rule Validation
# Check for invalid numeric values
# ------------------------------------------------------------

print("Negative sales records:")
silver.filter(col("sales") < 0).show()

print("Invalid quantity records:")
silver.filter(col("quantity") <= 0).show()

# ------------------------------------------------------------
# Dataset Summary
# ------------------------------------------------------------
print(f"Total Rows : {after_count}")
print(f"Columns    : {len(silver.columns)}")

silver.describe(
    "sales",
    "quantity",
    "discount",
    "profit"
).show()

# ------------------------------------------------------------
# Save Silver table in Delta format
# overwrite mode is used for development purposes
# ------------------------------------------------------------
(
    silver.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("workspace.salesdb.silver_sales")
)

# ------------------------------------------------------------
# Preview Silver table
# ------------------------------------------------------------
display(
    spark.read.table("workspace.salesdb.silver_sales")
)