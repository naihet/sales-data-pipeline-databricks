# Databricks notebook source
# DBTITLE 1,00_data_quality_check
bronze.count()
bronze.columns
bronze.printSchema()
bronze.describe().show()
bronze.selectExpr(
    "count(*) as total_rows"
).show()

# COMMAND ----------

# DBTITLE 1,01_load_bronze
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

df = (
    spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv("/Volumes/workspace/salesdb/raw_data/Sample - Superstore.csv")
)

df = df.toDF(*[
    col.lower().replace(" ", "_")
    for col in df.columns
])

display(df)
df.printSchema()
df.count()

df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("workspace.salesdb.bronze_sales")