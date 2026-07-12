# Databricks notebook source
%md
# ============================================================
# Spark SQL Analytics
#
# Purpose:
#   - Query Gold tables using Spark SQL.
#   - Generate business insights.
#   - Demonstrate SQL analytics on Delta tables.
# ============================================================

%sql
-- ============================================================
-- Query 1: Sales by Region
-- ============================================================

SELECT
    region,
    ROUND(total_sales,2) AS total_sales,
    ROUND(total_profit,2) AS total_profit
FROM workspace.salesdb.gold_sales_by_region
ORDER BY total_sales DESC;

-- ============================================================
-- Query 2: Monthly Sales Trend
-- ============================================================

SELECT
    order_month,
    ROUND(monthly_sales,2) AS monthly_sales
FROM workspace.salesdb.gold_monthly_sales
ORDER BY order_month;

-- ============================================================
-- Query 3: Top 10 Products
-- ============================================================

SELECT
    product_name,
    ROUND(total_sales, 2) AS total_sales
FROM workspace.salesdb.gold_top_products
ORDER BY total_sales DESC
LIMIT 10;

-- ============================================================
-- Query 4: Profit by Category
-- ============================================================

SELECT
    category,
    ROUND(SUM(sales),2) AS total_sales,
    ROUND(SUM(profit),2) AS total_profit
FROM workspace.salesdb.silver_sales
GROUP BY category
ORDER BY total_sales DESC;

-- ============================================================
-- Query 5: Sales by Segment
-- ============================================================

SELECT
    segment,
    ROUND(SUM(sales),2) AS total_sales,
    ROUND(SUM(profit),2) AS total_profit
FROM workspace.salesdb.silver_sales
GROUP BY segment
ORDER BY total_sales DESC;

-- ============================================================
-- Query 6: Top 10 Customers
-- ============================================================

SELECT
    customer_name,
    ROUND(SUM(sales),2) AS total_sales
FROM workspace.salesdb.silver_sales
GROUP BY customer_name
ORDER BY total_sales DESC
LIMIT 10;

-- ============================================================
-- Query 7: Shipping Mode Performance
-- ============================================================

SELECT
    ship_mode,
    ROUND(SUM(sales),2) AS total_sales,
    ROUND(AVG(profit),2) AS avg_profit
FROM workspace.salesdb.silver_sales
GROUP BY ship_mode
ORDER BY total_sales DESC;

-- ============================================================
-- Query 8: Monthly Profit
-- ============================================================

SELECT
    DATE_FORMAT(order_date,'yyyy-MM') AS order_month,
    ROUND(SUM(profit),2) AS total_profit
FROM workspace.salesdb.silver_sales
GROUP BY DATE_FORMAT(order_date,'yyyy-MM')
ORDER BY order_month;

-- ============================================================
-- Query 9: Average Discount by Category
-- ============================================================

SELECT
    category,
    ROUND(AVG(discount),3) AS avg_discount
FROM workspace.salesdb.silver_sales
GROUP BY category
ORDER BY avg_discount DESC;

-- ============================================================
-- Query 10: Dataset Summary
-- ============================================================

SELECT
    COUNT(*) AS total_orders,
    ROUND(SUM(sales),2) AS total_sales,
    ROUND(SUM(profit),2) AS total_profit,
    ROUND(AVG(discount),3) AS average_discount
FROM workspace.salesdb.silver_sales;