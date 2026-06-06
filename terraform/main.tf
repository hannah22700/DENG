terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.6.0"
    }
  }
}

provider "google" {
  project     = var.project
  region      = var.region
  credentials = file(var.credentials)
}


resource "google_storage_bucket" "bucket" {
  name          = var.gcs_bucket_name
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


resource "google_bigquery_dataset" "dataset" {
  dataset_id                 = var.bq_dataset_name
  location                   = var.location
  delete_contents_on_destroy = true
}


resource "google_bigquery_table" "votes" {
  dataset_id          = google_bigquery_dataset.dataset.dataset_id
  table_id            = "votes"
  schema              = file("${path.module}/schemas/votes.json")
  deletion_protection = false

  time_partitioning {
    type  = "DAY"
    field = "VoteEnd"
  }

  clustering = [
    "BusinessNumber"
  ]
}

resource "google_bigquery_table" "votings" {
  dataset_id          = google_bigquery_dataset.dataset.dataset_id
  table_id            = "votings"
  schema              = file("${path.module}/schemas/votings.json")
  deletion_protection = false
  time_partitioning {
    type  = "DAY"
    field = "VoteEnd"
  }

  clustering = [
    "IdVote"
  ]
}

resource "google_bigquery_table" "partysummary" {
  dataset_id          = google_bigquery_dataset.dataset.dataset_id
  table_id            = "partysummary"
  schema              = file("${path.module}/schemas/partysummary.json")
  deletion_protection = false
}
