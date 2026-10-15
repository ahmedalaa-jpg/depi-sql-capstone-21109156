import psycopg2
import sys
import os

# Add root directory to sys.path to import config.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import get_db_connection_params

def run_phase1():
    """Execute Phase 1: Environment & Database Connection Setup Validation."""
    print("\n[PHASE 1] Starting Project Setup & Database Connection Test...")
    
    try:
        # Load database parameters and establish connection
        params = get_db_connection_params()
        conn = psycopg2.connect(**params)
        cursor = conn.cursor()
        
        # Verify connection by retrieving PostgreSQL version
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()[0]
        
        print(f"  ✔ Successfully connected to database: '{params['dbname']}' on {params['host']}:{params['port']}")
        print(f"  ✔ PostgreSQL Engine: {db_version.split(',')[0]}")
        
        cursor.close()
        conn.close()
        print("[PHASE 1] Completed successfully: Environment and Connection Verified.\n")
        return True
        
    except Exception as e:
        print(f"  ❌ Phase 1 Failed - Connection Error: {e}")
        return False

if __name__ == '__main__':
    run_phase1()