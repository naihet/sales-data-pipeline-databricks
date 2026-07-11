# Databricks notebook source
# DBTITLE 1,03_build_gold
# ============================================================
# Gold Layer
# Purpose:
#   - Read cleaned data from the Silver layer.
#   - Aggregate business metrics for analytics and reporting.
#   - Create business-ready Gold tables.
#   - Store aggregated data in Delta format.
# ============================================================

from pyspark.sql.functions import (
    sum,
    date_format,
    desc
)

# ------------------------------------------------------------
# Read data from Silver layer
# ------------------------------------------------------------
silver = spark.read.table("workspace.salesdb.silver_sales")

# ============================================================
# Gold Table 1: Sales by Region
# ============================================================

# ------------------------------------------------------------
# Aggregate total sales and profit by region
# ------------------------------------------------------------
gold_region = (
    silver
    .groupBy("region")
    .agg(
        sum("sales").alias("total_sales"),
        sum("profit").alias("total_profit")
    )
    .orderBy(desc("total_sales"))
)

# Preview result
display(gold_region)

# Save Gold table
(
    gold_region.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("workspace.salesdb.gold_sales_by_region")
)

# ============================================================
# Gold Table 2: Monthly Sales
# ============================================================

# ------------------------------------------------------------
# Aggregate total sales by order month
# ------------------------------------------------------------
gold_monthly = (
    silver
    .withColumn(
        "order_month",
        date_format("order_date", "yyyy-MM")
    )
    .groupBy("order_month")
    .agg(
        sum("sales").alias("monthly_sales")
    )
    .orderBy("order_month")
)

# Preview result
display(gold_monthly)

# Save Gold table
(
    gold_monthly.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("workspace.salesdb.gold_monthly_sales")
)

# ============================================================
# Gold Table 3: Top Products
# ============================================================

# ------------------------------------------------------------
# Aggregate total sales by product
# ------------------------------------------------------------
gold_products = (
    silver
    .groupBy("product_name")
    .agg(
        sum("sales").alias("total_sales")
    )
    .orderBy(desc("total_sales"))
)

# Preview Top 10 products
display(gold_products.limit(10))

# Save Gold table
(
    gold_products.write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("workspace.salesdb.gold_top_products")
)

# ------------------------------------------------------------
# Verify Gold tables
# ------------------------------------------------------------

display(
    spark.read.table("workspace.salesdb.gold_sales_by_region")
)

display(
    spark.read.table("workspace.salesdb.gold_monthly_sales")
)

display(
    spark.read.table("workspace.salesdb.gold_top_products")
)