terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.42.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials)
  project     = var.project
  region      = var.region
}

resource "google_storage_bucket" "json_raw_data_bucket" {
  name          = var.gcs_bucket_raw_data
  location      = var.location
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "ecommerce-dataset" {
  dataset_id                  = var.bq_dataset_name
  description                 = "This dataset stores the transformed data of ecommerce data"
  location                    = var.location
}

resource "google_bigquery_table" "ods_ecommerce_products" {
  dataset_id = google_bigquery_dataset.ecommerce-dataset.dataset_id
  table_id   = var.gcs_dataset_table_name
}