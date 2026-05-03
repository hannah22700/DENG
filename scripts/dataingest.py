from google.cloud import storage
import time
import os

class gcs_connector:
    def __init__(self, credentials, bucketname):
        self.client = storage.Client.from_service_account_json(credentials)
        self.bucket = self.client.bucket(bucketname)


    def verify_gcs_upload(self, blob_name):
        return storage.Blob(bucket=self.bucket, name=blob_name).exists(self.client)


    def upload_to_gcs(self, file_path, chunk_size, max_retries=3):
        blob_name = os.path.basename(file_path)
        blob = self.bucket.blob(blob_name)
        blob.chunk_size = chunk_size

        for attempt in range(max_retries):
            try:
                print(f"Uploading {file_path} to {self.bucket.name} (Attempt {attempt + 1})...")
                blob.upload_from_filename(file_path)
                print(f"Uploaded: gs://{self.bucket.name}/{blob_name}")

                if self.verify_gcs_upload(blob_name):
                    print(f"Verification successful for {blob_name}")
                    return
                else:
                    print(f"Verification failed for {blob_name}, retrying...")
            except Exception as e:
                print(f"Failed to upload {file_path} to GCS: {e}")

            time.sleep(5)

        print(f"Giving up on {file_path} after {max_retries} attempts.")
