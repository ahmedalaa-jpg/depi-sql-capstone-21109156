import sys
from etl import run_pipeline

def main():
    """Main application entry point."""
    print("Initiating DEPI Capstone Workflow...")
    success = run_pipeline()
    
    if success:
        print("Status: SUCCESS - All pipeline phases completed.")
        sys.exit(0)
    else:
        print("Status: FAILED - Pipeline execution encountered errors.")
        sys.exit(1)

if __name__ == '__main__':
    main()