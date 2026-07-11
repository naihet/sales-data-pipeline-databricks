# ============================================================
# Bronze Layer
# Purpose:
#   - Load raw CSV data into the Bronze layer.
#   - Preserve the original dataset with minimal transformation.
#   - Store data in Delta format for downstream processing.
# ============================================================

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Get or create Spark session
spark = SparkSession.builder.getOrCreate()

# ------------------------------------------------------------
# Read raw CSV file
# - First row is the header
# - Automatically infer column data types
# ------------------------------------------------------------
df = (
    spark.read
        .option("header", True)
        .option("inferSchema", True)
        .option("quote", '"')
        .option("escape", '"')
        .option("multiLine", True)
        .csv("/Volumes/workspace/salesdb/raw_data/Sample - Superstore.csv")
)

# ------------------------------------------------------------
# Standardize column names
# Convert:
#   Order ID -> order_id
#   Ship Date -> ship_date
# ------------------------------------------------------------
df = df.toDF(*[
    c.strip()
     .lower()
     .replace(" ", "_")
     .replace("-", "_")
    for c in df.columns
])

# Preview dataset
display(df)

# Inspect schema
df.printSchema()

# Verify total number of records
df.count()

# ------------------------------------------------------------
# Save Bronze table in Delta format
# overwrite mode is used for development purposes
# ------------------------------------------------------------
df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("workspace.salesdb.bronze_sales")