import csv
import psycopg2
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import get_db_connection_params

def run_phase2():
    print("\n[PHASE 2] Starting Data Understanding & Structural Audit...")
    
    params = get_db_connection_params()
    conn = psycopg2.connect(**params)
    cursor = conn.cursor()

    # 1. Quality Audit
    audit_targets = [
        ("orders", "order_id"),
        ("orders", "order_delivered_customer_date"),
        ("orders", "order_estimated_delivery_date"),
        ("order_items", "price"),
        ("order_items", "freight_value"),
        ("products", "product_category_name"),
        ("customers", "customer_zip_code_prefix")
    ]
    
    audit_rows = [("table_name", "column_name", "null_count", "total_rows", "null_percentage")]
    for table_name, col_name in audit_targets:
        query = f"""
            SELECT '{table_name}', '{col_name}', 
                   COUNT(*) - COUNT({col_name}), 
                   COUNT(*), 
                   ROUND((COUNT(*) - COUNT({col_name}))::DECIMAL / COUNT(*) * 100, 2)
            FROM {table_name};
        """
        cursor.execute(query)
        audit_rows.append(cursor.fetchone())

    # Ensure outputs directory exists
    os.makedirs('outputs', exist_ok=True)
    
    with open('outputs/phase2_quality_audit.csv', 'w', newline='', encoding='utf-8') as f:
        csv.writer(f).writerows(audit_rows)
    print("  ✔ Exported outputs/phase2_quality_audit.csv")

    # 2. EDA Statistics
    eda_query = """
        SELECT 'order_items', 'price', MIN(price)::NUMERIC(10,2), MAX(price)::NUMERIC(10,2), AVG(price)::NUMERIC(10,2), STDDEV(price)::NUMERIC(10,2), COUNT(*) FROM order_items
        UNION ALL
        SELECT 'order_items', 'freight_value', MIN(freight_value)::NUMERIC(10,2), MAX(freight_value)::NUMERIC(10,2), AVG(freight_value)::NUMERIC(10,2), STDDEV(freight_value)::NUMERIC(10,2), COUNT(*) FROM order_items
        UNION ALL
        SELECT 'order_payments', 'payment_value', MIN(payment_value)::NUMERIC(10,2), MAX(payment_value)::NUMERIC(10,2), AVG(payment_value)::NUMERIC(10,2), STDDEV(payment_value)::NUMERIC(10,2), COUNT(*) FROM order_payments;
    """
    cursor.execute(eda_query)
    eda_rows = [["table_name", "metric_column", "min_val", "max_val", "avg_val", "stddev_val", "total_records"]] + cursor.fetchall()

    with open('outputs/phase2_eda_summary.csv', 'w', newline='', encoding='utf-8') as f:
        csv.writer(f).writerows(eda_rows)
    print("  ✔ Exported outputs/phase2_eda_summary.csv")

    cursor.close()
    conn.close()
    print("[PHASE 2] Completed successfully.\n")

if __name__ == '__main__':
    run_phase2()