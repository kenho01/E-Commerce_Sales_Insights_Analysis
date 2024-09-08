variable "credentials" {
  description = "My Credentials"
  default     = "./keys/mycreds.json"
}

variable "project" {
  description = "Project"
  default     = "ecommerce-insights-435001"
}

variable "region" {
  description = "Region"
  default     = "us-central1"
}

variable "location" {
  description = "Project Location"
  default     = "US"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "ecommerce_dataset"
}

variable "gcs_bucket_raw_data" {
  description = "Storage bucket for raw json data"
  default     = "ecommerce-insights-435001-raw-json-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}

variable "gcs_dataset_table_name" {
  description = "Table name"
  default     = "ods_ecommerce_products"
}