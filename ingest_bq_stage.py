import os
import pandas as pd
import scripts.clouddataingest as di
from dotenv import load_dotenv
from io import StringIO

load_dotenv()

FILE_PATH = "output"
CREDENTIALS_FILE = os.getenv("ENV_GOOGLE_CREDENTIALS")
PROJECT_NAME = os.getenv("ENV_PROJECT_NAME")
BUCKET_NAME = os.getenv("ENV_BUCKET_NAME")
BIGQUERY_NAME = os.getenv("ENV_BIGQUERY_NAME")

date = '2026.05.07'

def main():

    print("Starting Pipeline")
    gcsc = di.gcs_connector(CREDENTIALS_FILE, BUCKET_NAME)
    gbq = di.gbq_connector(CREDENTIALS_FILE,BIGQUERY_NAME, PROJECT_NAME)

    blobs = gcsc.get_blobs()

    for blob in blobs:
        tablename = blob.name.split("_")[0]
        blobdate = blob.name.split("_")[3]

        if (date.replace(".","")  == blobdate ):
            data = gcsc.get_from_gcs(blob.name)
            
            df = pd.read_csv(StringIO(data))

            gbq.load_data(df, f"stg_{tablename}")


if __name__ == "__main__":
    main()
