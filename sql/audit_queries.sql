-- 1. Baseline Record Counts
SELECT 'orders' AS table_nam, COUNT(*) AS total_rows FROM orders
UNION ALL
SELECT 'order_items', COUNT(*) FROM order_items
UNION ALL
SELECT 'order_payments', COUNT(*) FROM order_payments
UNION ALL
SELECT 'customers', COUNT(*) FROM customers
UNION ALL
SELECT 'products', COUNT(*) FROM products;

-- 2. Data Quality Audit (Missing Values)
SELECT 
    'orders' AS table_name,
    'order_delivered_customer_date' AS column_name,
    COUNT(*) - COUNT(order_delivered_customer_date) AS null_count,
    COUNT(*) AS total_rows,
    ROUND((COUNT(*) - COUNT(order_delivered_customer_date))::DECIMAL / COUNT(*) * 100, 2) AS null_percentage
FROM orders;

-- 3. Descriptive Statistics (EDA Summary)
SELECT 'order_items' AS table_name, 'price' AS metric_column, 
       MIN(price)::NUMERIC(10,2) AS min_val, 
       MAX(price)::NUMERIC(10,2) AS max_val, 
       AVG(price)::NUMERIC(10,2) AS avg_val, 
       STDDEV(price)::NUMERIC(10,2) AS stddev_val,
       COUNT(*) AS total_records
FROM order_items
UNION ALL
SELECT 'order_items', 'freight_value', 
       MIN(freight_value)::NUMERIC(10,2), 
       MAX(freight_value)::NUMERIC(10,2), 
       AVG(freight_value)::NUMERIC(10,2), 
       STDDEV(freight_value)::NUMERIC(10,2),
       COUNT(*)
FROM order_items
UNION ALL
SELECT 'order_payments', 'payment_value', 
       MIN(payment_value)::NUMERIC(10,2), 
       MAX(payment_value)::NUMERIC(10,2), 
       AVG(payment_value)::NUMERIC(10,2), 
       STDDEV(payment_value)::NUMERIC(10,2),
       COUNT(*)
FROM order_payments;