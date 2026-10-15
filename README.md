# depi-sql-capstone-21109156
# Olist E-Commerce Production ETL & Feature Store Pipeline

An end-to-end, production-ready ETL pipeline for the Olist Brazilian E-Commerce dataset built using Python (`psycopg2`) and PostgreSQL, following the **CRISP-DM** (Cross-Industry Standard Process for Data Mining) methodology.

---

## 📌 Project Architecture & Methodology

This project follows the CRISP-DM lifecycle, transitioning seamlessly from interactive exploratory notebooks to modular python production scripts.

.
├── config.py                  # Database connection configuration loader
├── etl.py                     # Pipeline master orchestrator
├── main.py                    # Application execution entry point
├── requirements.txt           # Project dependencies
├── notebooks/
│   ├── 01_eda_scratchpad.ipynb          # Phase 1 & 2 exploratory analysis
│   └── 02_feature_engineering_test.ipynb# Phase 3 cleaning & feature testing
├── outputs/
│   ├── phase2_quality_audit.csv         # Missing values defect analysis
│   └── phase2_eda_summary.csv           # Baseline summary statistics
├── scripts/
│   ├── phase1.py              # Environment & DB connection validator
│   ├── phase2.py              # Data audit & EDA automated exporter
│   └── phase3.py              # SQL cleaning & Feature Store builder
└── sql/
├── audit_queries.sql      # Diagnostic & EDA queries
├── data_cleaning.sql      # Whitespace TRIM & CTID deduplication
└── feature_store.sql      # Feature engineering & target table creation

---

## 🛠️ Tech Stack & Prerequisites

* **Database Engine:** PostgreSQL 18.x
* **Language:** Python 3.14+
* **Database Driver:** `psycopg2`
* **Environment Management:** `python-dotenv`

---

## 🔄 CRISP-DM Execution Pipeline

### Phase 1: Business Understanding & Setup
- Environment verification and PostgreSQL database connection validation.
- Standardized configuration handling using environment variables.

### Phase 2: Data Understanding
- Structural schema audit across all core user tables.
- Automated quality defect audit capturing NULL percentage distributions.
- Aggregated descriptive statistics saved to `outputs/`.

### Phase 3: Data Preparation & Feature Engineering
- In-database text standardization (`LOWER`, `TRIM`) across city, state, and payment fields.
- Duplicate record removal using PostgreSQL Window Functions (`ROW_NUMBER()` over `CTID`).
- Feature Store construction (`feature_store_olist`) with delivery durations, seller-customer geographic matching, and payment aggregations.
- Target variable creation: `is_late_delivery` (1 if actual delivery exceeded estimated date, 0 otherwise).

---

## 🚀 How to Run the Pipeline

1. **Configure Environment:**
   Ensure your `.env` file contains your PostgreSQL connection parameters:
   ```env
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=olist_messy_db
   DB_USER=postgres
   DB_PASSWORD=your_password