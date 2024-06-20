variable "credentials" {
  default     = "./keys/my-creds.json"
  description = "Project credentials"
}

# project
variable "project" {
  default     = "data-pipeline"
  description = "Project Name"
}

# region
variable "region" {
  default     = "us-central1"
  description = "Project Region"
}

# location
variable "location" {
  default     = "US"
  description = "Project Location"
}

# Cloud run
variable "cloud_run_job" {
  default     = "scrapy-tf"
  description = "cloud run job"
}

# google storage 
variable "gcs_bucket_name" {
  default     = "de-zoomcamp-bucket-1"
  description = "Bucket Name"
}

# Dataproc cluster
variable "dataproc_cluster_name" {
  default     = "pyspark-analysis"
  description = "Dataproc Cluster"
}

# BigQuery
variable "bq_dataset_name" {
  default     = "dubai_real_estate"
  description = "BigQuery datasets"
}

# Cloud Composer 
variable "cloud_composer_env" {
  default     = "project-datapipeline"
  description = "Cloud composer"
}

