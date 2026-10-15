import psycopg2
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import get_db_connection_params

def run_phase3():
    """Execute Phase 3: Data Cleaning and Feature Store Creation."""
    print("\n[PHASE 3] Starting Data Preparation & Feature Store Pipeline...")
    
    try:
        params = get_db_connection_params()
        conn = psycopg2.connect(**params)
        cursor = conn.cursor()

        # 1. Execute Data Cleaning
        print("  -> Executing data cleaning queries...")
        with open('sql/data_cleaning.sql', 'r', encoding='utf-8') as f:
            cursor.execute(f.read())
        conn.commit()
        print("  ✔ Data cleaning completed.")

        # 2. Execute Feature Store Creation
        print("  -> Constructing feature store table...")
        with open('sql/feature_store.sql', 'r', encoding='utf-8') as f:
            cursor.execute(f.read())
        conn.commit()
        print("  ✔ Feature store table 'feature_store_olist' successfully built.")

        cursor.close()
        conn.close()
        print("[PHASE 3] Completed successfully.\n")
        return True

    except Exception as e:
        print(f"  ❌ Phase 3 Failed: {e}")
        return False

if __name__ == '__main__':
    run_phase3()