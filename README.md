# Renewable Energy Data Pipeline

## 📌 Overview
This project builds an end-to-end data pipeline to process, clean, and analyze European electricity demand and renewable energy production data. The pipeline transforms raw, messy time-series data into structured datasets for analysis and visualization.

---

## 🎯 Goal
To design and implement a scalable data pipeline that enables analysis of how renewable energy (wind & solar) impacts electricity demand patterns across Europe.

---

## 📚 Table of Contents

- [Overview](#-overview)  
- [Goal](#-goal)  
- [Problem Statement](#-problem-statement)  
- [Architecture](#-architecture)  
- [Tech Stack](#-tech-stack)  
- [Pipeline Steps](#-pipeline-steps)  
- [Project Structure](#-project-structure)  
- [Expected Output](#-expected-output)  
- [Future Improvements](#-future-improvements)  

---

## ❓ Problem Statement
This project aims to answer:

- How does electricity demand vary over time?
- What share of energy comes from renewable sources?
- When do peak demand periods occur?
- How clean and reliable is real-world energy data?

---

## 🏗️ Architecture
The pipeline follows a modern data engineering architecture with clear separation of responsibilities between orchestration, storage, and transformation layers:

External Data Source (CSV)
        ↓
Airflow (Ingestion & Orchestration)
        ↓
Google Cloud Storage (Data Lake - Raw Layer)
        ↓
BigQuery (Raw Tables)
        ↓
dbt (Staging & Transformations)
        ↓
BigQuery (Analytics Tables)
        ↓
Looker Studio (Visualization)

---

## ⚙️ Tech Stack

- **Orchestration:** Apache Airflow  
- **Programming Language:** Python (Pandas)  
- **Data Lake:** Google Cloud Storage (GCS)  
- **Data Warehouse:** BigQuery  
- **Transformation:** dbt  
- **Containerization:** Docker  
- **Infrastructure as Code:** Terraform  
- **Visualization:** Looker Studio  

---

## 🔄 Pipeline Steps

1. **Ingestion**
   - Download raw energy dataset
   - Store in GCS (data lake)

2. **Transformation**
   - Clean missing values
   - Standardize timestamps
   - Select relevant features (demand, wind, solar)
   - Create new features (hour, day, renewable share)

3. **Storage**
   - Convert to Parquet
   - Load into BigQuery

4. **Analysis**
   - Aggregate daily metrics
   - Identify peak demand periods
   - Compare renewable vs total energy

5. **Visualization**
   - Build dashboard in Looker Studio

---

## 📂 Project Structure
```text
renewable-energy-pipeline/
│
├── airflow/
│   └── dags/
│       └── energy_pipeline.py          # Main Airflow DAG
│
├── dbt/
│   └── energy_project/
│       ├── models/
│       │   ├── staging/
│       │   │   └── stg_energy.sql      # Cleaned raw data
│       │   └── marts/
│       │       └── energy_metrics.sql  # Aggregated metrics
│       │
│       ├── seeds/                      # Optional static data
│       ├── tests/                      # dbt tests
│       ├── dbt_project.yml
│       └── profiles.yml
│
├── src/
│   ├── ingest.py                       # Data download logic
│   ├── validate.py                     # Data validation checks
│   └── utils.py                        # Helper functions
│
├── data/
│   ├── raw/                            # Local raw files (optional)
│   └── processed/                      # Local processed files
│
├── terraform/
│   ├── main.tf                         # GCP resources (GCS, BigQuery)
│   └── variables.tf
│
├── docker/
│   └── Dockerfile                      # Custom container (optional)
│
├── notebooks/
│   └── exploration.ipynb               # EDA (not part of pipeline)
│
├── docker-compose.yaml                 # Orchestration (Airflow, dbt, etc.)
├── requirements.txt                    # Python dependencies
├── .env                                # Environment variables (not committed)
└── README.md
```
---

## 📊 Expected Output

- Cleaned Parquet datasets  
- Aggregated energy metrics  
- BigQuery tables  
- Interactive dashboard  

---

## 🚀 Future Improvements

- Add weather data integration  
- Implement real-time data ingestion  
- Improve data quality checks  
- Add anomaly detection  
