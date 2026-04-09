# -----------------------
# Provider
# -----------------------
provider "google" {
  project = var.project_id
  region  = var.region
}

# -----------------------
# GCS Bucket (Data Lake)
# -----------------------
resource "google_storage_bucket" "energy_bucket" {
  name     = var.bucket_name   # energy-pipeline-bucket
  location = var.region

  uniform_bucket_level_access = true
  force_destroy               = true

  labels = {
    project     = "energy-pipeline"
    environment = var.environment
  }
}

# -----------------------
# BigQuery Dataset
# -----------------------
resource "google_bigquery_dataset" "energy_dataset" {
  dataset_id = var.dataset_id   # energy_pipeline_dataset
  location   = var.region

  delete_contents_on_destroy = true

  labels = {
    project     = "energy-pipeline"
    environment = var.environment
  }
}