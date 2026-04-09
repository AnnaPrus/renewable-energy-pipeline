variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "europe-west1"
}

variable "bucket_name" {
  description = "GCS bucket name"
  type        = string
  default     = "energy-pipeline-bucket"
}

variable "dataset_id" {
  description = "BigQuery dataset ID"
  type        = string
  default     = "energy_pipeline_dataset"
}

variable "environment" {
  description = "Environment (dev/prod)"
  type        = string
  default     = "dev"
}