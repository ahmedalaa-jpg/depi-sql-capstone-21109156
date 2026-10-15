import sys
import os

from scripts.phase1 import run_phase1
from scripts.phase2 import run_phase2
from scripts.phase3 import run_phase3

def run_pipeline():
    """Execute the complete end-to-end DEPI Capstone ETL & Feature Engineering Pipeline."""
    print("=" * 65)
    print("🚀 Starting DEPI Capstone E-Commerce Pipeline")
    print("=" * 65)
    
    # Step 1: Run Phase 1 (Environment & DB Check)
    if not run_phase1():
        print("❌ Pipeline halted at Phase 1.")
        return False

    # Step 2: Run Phase 2 (Audit & EDA)
    run_phase2()

    # Step 3: Run Phase 3 (Cleaning & Feature Store Construction)
    if not run_phase3():
        print("❌ Pipeline halted at Phase 3.")
        return False

    print("=" * 65)
    print("🎉 End-to-End Pipeline Executed Successfully!")
    print("=" * 65)
    return True

if __name__ == '__main__':
    run_pipeline()