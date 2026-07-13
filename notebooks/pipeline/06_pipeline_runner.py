# Databricks notebook source
# ============================================================
# Pipeline Runner
# Purpose:
#   - Execute the complete data pipeline in sequence.
#   - Run Bronze, Silver, Gold, and Data Quality notebooks.
#   - Simulate a production ETL workflow.
# ============================================================

# ------------------------------------------------------------
# Execute Bronze Layer
# ------------------------------------------------------------

dbutils.notebook.run(
    "../bronze/01_load_bronze",
    timeout_seconds=600
)

# ------------------------------------------------------------
# Execute Silver Layer
# ------------------------------------------------------------

dbutils.notebook.run(
    "../silver/02_clean_silver",
    timeout_seconds=600
)

# ------------------------------------------------------------
# Execute Gold Layer
# ------------------------------------------------------------

dbutils.notebook.run(
    "../gold/03_build_gold",
    timeout_seconds=600
)

# ------------------------------------------------------------
# Execute Data Quality Report
# ------------------------------------------------------------

dbutils.notebook.run(
    "--/quality/05_data_quality_report",
    timeout_seconds=600
)

print("=" * 50)
print("Pipeline completed successfully.")
print("=" * 50)