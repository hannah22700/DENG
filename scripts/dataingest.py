from google.cloud import storage
from google.cloud import bigquery
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

    def get_from_gcs(self, path):
        blob = self.bucket.blob(path)
        data = blob.download_as_text()
        return data
    
    def get_blobs(self):
        blobs = self.client.list_blobs( self.bucket.name)
        return blobs
    

class gbq_connector:
     def __init__(self, credentials, bigqueryname , projectname):
        self.client = bigquery.Client.from_service_account_json(credentials)
        self.datasetname = bigqueryname
        self.projecname = projectname

    
     def load_data(self, df, table):
        table_id = f"{self.projecname}.{self.datasetname}.{table}"
        job = self.client.load_table_from_dataframe(df, table_id)


        return job.result()

    

