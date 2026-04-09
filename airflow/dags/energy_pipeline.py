import os
import requests
from airflow import DAG
from airflow.decorators import task
import pendulum
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
import pandas as pd
from airflow.models import Variable
import logging

# -----------------------
# Config
# -----------------------
BASE_URL = "https://data.open-power-system-data.org/time_series"
VERSION = "2020-10-06"

DATA_URL = f"{BASE_URL}/{VERSION}/time_series_60min_singleindex.csv"

DATA_DIR = "/opt/airflow/data"
FILE_NAME = "energy_raw.csv"
LOCAL_PATH = os.path.join(DATA_DIR, FILE_NAME)
CLEAN_FILE_NAME = "energy_clean.csv"
CLEAN_PATH = os.path.join(DATA_DIR, CLEAN_FILE_NAME)

BUCKET_NAME = Variable.get("gcp_bucket", default_var="energy-pipeline-bucket")
PROJECT_ID = Variable.get("gcp_project", default_var="energy-pipeline-492713")
DATASET_ID = Variable.get("bq_dataset", default_var="energy_pipeline_dataset")

TABLE_ID = "energy_clean"

default_args = {
    "retries": 2,
    "retry_delay": pendulum.duration(minutes=5),
}

# -----------------------
# DAG
# -----------------------
with DAG(
    dag_id="renewable_energy_pipeline",
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
    tags=["energy", "ingestion"],
) as dag:

    @task
    def download_data():
        os.makedirs(DATA_DIR, exist_ok=True)
        temp_path = LOCAL_PATH + ".tmp"

        logging.info(f"Downloading data from: {DATA_URL}")
        response = requests.get(DATA_URL, timeout=60)

        if response.status_code != 200:
            msg = f"Download failed with status {response.status_code}"
            logging.error(msg)
            raise Exception(msg)

        with open(temp_path, "wb") as f:
            f.write(response.content)

        # then rename
        os.replace(temp_path, LOCAL_PATH)

        logging.info(f"File saved to: {LOCAL_PATH}")

    download_task = download_data()

    @task
    def clean_data():
        logging.info("Cleaning data started")

        df = pd.read_csv(LOCAL_PATH)

        # -----------------------
        # Basic cleaning
        # -----------------------

        logging.info("Cleaning data...")
        logging.info(f"Initial shape: {df.shape}")
        # 1. Drop completely empty columns
        df = df.dropna(axis=1, how="all")

        # 2. Convert timestamp
        df["utc_timestamp"] = pd.to_datetime(df["utc_timestamp"], errors="coerce")

        # 3. Drop rows without timestamp
        df = df.dropna(subset=["utc_timestamp"])

        # 4. Limit columns (IMPORTANT for BigQuery)
        selected_cols = [
            "utc_timestamp",
            "DE_load_actual_entsoe_transparency",
            "DE_solar_generation_actual",
            "DE_wind_onshore_generation_actual",
            "AT_load_actual_entsoe_transparency",
            "AT_solar_generation_actual",
            "AT_wind_onshore_generation_actual",
        ]

        df = df[selected_cols]

        # -----------------------
        # Save cleaned file
        # -----------------------
        df.to_csv(CLEAN_PATH, index=False)
        logging.info(f"Final shape: {df.shape}")
        logging.info(f"Columns: {list(df.columns)}")
        logging.info(f"Cleaned file saved to: {CLEAN_PATH}")

        return CLEAN_PATH
    
    clean_task = clean_data()

    # -----------------------
    # Validate data
    # -----------------------
    @task
    def validate_data(path):
        df = pd.read_csv(path)

        logging.info("Validating data...")
        if df.empty:
            logging.error("Dataset is empty")
            raise ValueError("Dataset is empty")

        if df["utc_timestamp"].isnull().any():
            logging.error("Null timestamps found")
            raise ValueError("Null timestamps found")
        
        logging.info("Validation passed")
        return path
    
    validate_task = validate_data(clean_task)
    # -----------------------
    # Upload to GCS
    # -----------------------
    upload_to_gcs = LocalFilesystemToGCSOperator(
        task_id="upload_to_gcs",
        src=CLEAN_PATH,
        dst=f"raw/{CLEAN_FILE_NAME}",
        bucket=BUCKET_NAME,
        gcp_conn_id="google_cloud_default",
    )
    # -----------------------
    # Upload to BigQuery
    # -----------------------
    load_to_bq = GCSToBigQueryOperator(
        task_id="load_to_bq",
        bucket=BUCKET_NAME,
        source_objects=["raw/energy_clean.csv"],
        destination_project_dataset_table=f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}",
        source_format="CSV",
        skip_leading_rows=1,
        write_disposition="WRITE_TRUNCATE",
        autodetect=True,
        time_partitioning={"type": "DAY", "field": "utc_timestamp"},
        gcp_conn_id="google_cloud_default",
    )
    # -----------------------
    # Pipeline order
    # -----------------------
    download_task >> clean_task >> validate_task >> upload_to_gcs >> load_to_bq