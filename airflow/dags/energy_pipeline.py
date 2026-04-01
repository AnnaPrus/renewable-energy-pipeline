import os
import requests
from airflow import DAG
from airflow.decorators import task
import pendulum

# -----------------------
# Config
# -----------------------
BASE_URL = "https://data.open-power-system-data.org/time_series"
VERSION = "2020-10-06"

DATA_URL = f"{BASE_URL}/{VERSION}/time_series_60min_singleindex.csv"

DATA_DIR = "/opt/airflow/data"
FILE_NAME = "energy_raw.csv"
LOCAL_PATH = os.path.join(DATA_DIR, FILE_NAME)

# -----------------------
# DAG
# -----------------------
with DAG(
    dag_id="renewable_energy_pipeline",
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    schedule_interval=None,
    catchup=False,
    tags=["energy", "ingestion"],
) as dag:

    @task
    def download_data():
        os.makedirs(DATA_DIR, exist_ok=True)

        print(f"Downloading data from: {DATA_URL}")

        response = requests.get(DATA_URL)

        if response.status_code != 200:
            raise Exception(f"Download failed with status {response.status_code}")

        with open(LOCAL_PATH, "wb") as f:
            f.write(response.content)

        print(f"File saved to: {LOCAL_PATH}")

    download_data()