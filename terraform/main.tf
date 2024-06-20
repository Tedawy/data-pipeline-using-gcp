terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.25.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials)
  project     = var.project
  region      = var.region
}

# Artifact Registry
resource "google_artifact_registry_repository" "my_repo" {
  location      = var.region
  repository_id = var.project
  description   = "Docker repository for storing my Docker images"
  format        = "DOCKER"
}

# Code to push Docker image to Artifact Registry
resource "null_resource" "push_image_to_repo" {
  provisioner "local-exec" {
    command = <<EOT
      gcloud auth configure-docker
      docker push us-central1-docker.pkg.dev/data-pipeline/de-zoomcamp-repo/scrapy-project-image:latest
    EOT
  }

  depends_on = [google_artifact_registry_repository.my_repo]
}

# Cloud Run Job
resource "google_cloud_run_v2_job" "scrapy_service" {
  name     = var.cloud_run_job
  location = "us-central1"

  template {
    template {
      containers {
        image = "us-central1-docker.pkg.dev/data-pipeline/de-zoomcamp-repo/scrapy-project-image:latest"
        resources {
          limits = {
            cpu    = "2"
            memory = "1024Mi"
          }
        }
      }
      timeout = "3600s" # Set the timeout to 1 hour (3600 seconds)
    }
  }

  lifecycle {
    ignore_changes = [
      launch_stage,
    ]
  }
  depends_on = [null_resource.push_image_to_repo]
}

# google storage bucket
resource "google_storage_bucket" "data-lake-bucket" {
  name     = var.gcs_bucket_name
  location = var.location

  storage_class               = "STANDARD"
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30 // days
    }
  }

  force_destroy = true
}




# Dataproc Cluster
resource "google_dataproc_cluster" "cluster-111" {
  name   = var.dataproc_cluster_name
  region = var.region
  
  cluster_config {
    master_config {
      num_instances = 1
      machine_type = "n1-standard-2"
    }

    worker_config {
      num_instances = 2
      machine_type = "n1-standard-2"
    }

    initialization_action {
      script = "gs://dataproc-initialization-actions/jupyter/jupyter.sh"
    }
  }
}

# BigQuery 
resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.bq_dataset_name
  project    = var.project
  location   = var.location
}


# Service account permissions required for Cloud Composer
resource "google_service_account_iam_member" "custom_service_account" {
  provider           = google-beta
  service_account_id = "projects/data-pipeline/serviceAccounts/terraform-runner@data-pipeline.iam.gserviceaccount.com"
  role               = "roles/composer.ServiceAgentV2Ext"
  member             = "serviceAccount:{project_number}@cloudcomposer-accounts.iam.gserviceaccount.com"
}


# Cloud Composer 
resource "google_composer_environment" "data-pipeline" {
  provider = google-beta
  name     = var.cloud_composer_env
  project  = var.project
  region   = var.region
  
  config {
    software_config {
      image_version = "composer-3-airflow-2.7.3-build.5"
    }

    node_config {
      service_account = "terraform-runner@data-pipeline.iam.gserviceaccount.com"
    }

    workloads_config {
      scheduler {
        cpu        = 1
        memory_gb  = 4
        storage_gb = 5
        count      = 2
      }
      triggerer {
        count     = 1
        cpu       = 0.5
        memory_gb = 1
      }
      web_server {
        cpu        = 2
        memory_gb  = 7.5
        storage_gb = 5
      }
      worker {
        cpu        = 2
        memory_gb  = 7.5
        storage_gb = 10
        min_count  = 2
        max_count  = 4
      }
    }
    environment_size = "ENVIRONMENT_SIZE_MEDIUM"
  }
}
