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
Raw CSV → Ingestion → Cleaning → Transformation → Data Lake (GCP) → Data Warehouse (BigQuery) → Visualization

---

## ⚙️ Tech Stack

- **Cloud Platform:** Google Cloud Platform (GCP)
- **Data Lake:** Google Cloud Storage (GCS)
- **Data Warehouse:** BigQuery  
- **Orchestration:** Airflow  
- **Processing:** PySpark / Pandas  
- **Transformation:** dbt (optional)  
- **Infrastructure:** Terraform  
- **Containerization:** Docker  
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

renewable-energy-pipeline/
│
├── data/
│ ├── raw/
│ ├── processed/
│
├── src/
│ ├── ingest.py
│ ├── transform.py
│ ├── load.py
│
├── airflow/
├── terraform/
├── docker/
├── notebooks/
│
├── README.md
└── requirements.txt

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
