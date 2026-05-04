import os
import pandas as pd
import scripts.dataconnector as dc
import scripts.dataingest as di
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

FILE_PATH = "output"
CREDENTIALS_FILE = os.getenv("ENV_GOOGLE_CREDENTIALS")
PROJECT_NAME = os.getenv("ENV_PROJECT_NAME")
BUCKET_NAME = os.getenv("ENV_BUCKET_NAME")
CHUNK_SIZE = 8 * 1024 * 1024

since = "2026.03.12"
until = "2026.04.03"
now = datetime.now().strftime("%Y%m%d_%H%M%S")

def main():
    os.makedirs(FILE_PATH, exist_ok=True)

    gcsc = di.gcs_connector(CREDENTIALS_FILE, BUCKET_NAME)

    print("Starting Pipeline")

    __location__ = os.path.realpath(os.getcwd())
    path = os.path.join(__location__, "voting")

    print("Getting votes...")
    votes = dc.get_votes(since, until)

    dfvotes = pd.DataFrame(votes)

    print(f"Got {len(dfvotes)} Votes")
    
    dfvotes.to_csv(f"{FILE_PATH}/votes_{since}_{until}_{now}.csv")

    print("Uploading Votes")
    gcsc.upload_to_gcs(f"{FILE_PATH}/votes_{since}_{until}_{now}.csv", CHUNK_SIZE)

    if(len(dfvotes) > 0):
        print("Getting vortings...")
        dfvoting = dc.get_voting_of_votes(votes, path)

        dfvoting.to_csv(f"{FILE_PATH}/votings_{since}_{until}_{now}.csv")
        print(f"Got {len(dfvoting)} Votings")

        print("Uploading Votings")
        gcsc.upload_to_gcs(f"{FILE_PATH}/votings_{since}_{until}_{now}.csv", CHUNK_SIZE)
    else:
        print("No votings to ingest")



if __name__ == "__main__":
    main()
