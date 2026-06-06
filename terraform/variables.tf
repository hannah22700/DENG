variable "credentials" {
  description = "My Credentials"
  default     = "/secrets/google-key.json"

}


variable "project" {
  description = "Project"
  default     = "awesome-gate-489312-g2"
}

variable "region" {
  description = "Region"
  default     = "us-central1"
}

variable "location" {
  description = "Project Location"
  default     = "EU"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "bq_legislens_01"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "bu_legislens_03"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}
