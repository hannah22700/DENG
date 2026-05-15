# DENG

## Project Structure

The directory structure and important files are liste here:

```
.
├── flows                             # Contains Kestra Flows
│   |── openparl_ingest_bigquery.yml  # Kestra Flow
|   |── openparl_ingest_datalake.yml  # Kestra Flow
|   └── openparl_ingest_local.yml     # Kestra Flow
├── media                             # Contains Images for documentation
├── scripts                           # Contains Scripts for the kestra flows
│   ├── clouddataingest.py            # Data Ingestion for the cloud
│   ├── dataconnector.py              # Data Extraction from openparl
│   ├── datatransform.py              # Data Transformation
|   └── localdataingest.py            # Data Ingestion for the local postgres db
├── sql                               # Contains sample SQL Scripts
|── terraform                         # Contains IaC for Google Cloud Resources
|   ├── schemas                       # Contains Schmeas for big query tables
|   |   ├── partysummary.json         # Schema of the partysummary table
|   |   ├── votes.json                # Schema of the votes table
|   |   └── votings.json              # Schema of the votings table
|   ├── main.tf                       # Terraform file to create storage bucket and big query
|   └── variables.tf                  # Contains the variables for main.tf
├── docker-compose.yml                # Docker Compose file
├── Dockerfile_cloud.kestra           # Docker file for Kestra that installs dependencies for the cloud pipelines
├── Dockerfile_local.kestra           # Docker file for Kestra that installs dependencies for the local pipelines
├── ingest_bq_stage.py                # Script to stage data in the big query
|── ingest_datalake.py                # Script to collect data from openparl and write it to a datalake
|── ingest_local.py                   # Script to collect data from openparl and write it to the local postgres db
├── persona.md                        # description of our persona
├── pyproject.toml                    # virtual environment configuration
├── README.md                         # README
└── uv.lock                           # virtaul environment configuration
```

## Instructions to start local pipeline

### Prerequisites

For the pipeline to be run locally the following componentes have to be installed:

- Docker
- Docker Compose
- uv

### Instructions

First clone this repository to be able to start the pipeline locally:
Navigate to the directory where you want to clone the repo and run the following command:  
`git clone https://github.com/hannah22700/DENG.git`

Navigate inside the repo:  
`cd DENG`

Ensure that you have a working .env file. For reference .env_example can be found in the repo. For an easy set up, copy it and rename it to .env.

The following .env variables are relevant for the local set up:

```
KESTRA_USERNAME
KESTRA_PASSWORD
KESTRA_POSTGRES_USERNAME
KESTRA_POSTGRES_PASSWORD
ENV_POSTGRES_USERNAME
ENV_POSTGRES_PASSWORD
PGADMIN_DEFAULT_EMAIL
PGADMIN_DEFAULT_PASSWORD
```

After that start the neccessary containers with docker compose:

Start it with:  
`docker compose up -d`

Wait until the containers finished starting.

To start the pipeline locally without orchestration the `main.py` can be used.

Make sure you have uv installed, for the command to work.

Start the local pipeline with:

```
uv run main.py --voteCount=10
```

The parameter voteCount is used to control the number of votes that votings will be collected from. If the number is two large the pipeline will take very long.

### Verify pipeline result

To verify the result of the pipeline the postgres database is accessible with pgadmin:
https://localhost:8085

Username: admin@admin.com
Password: root

In pgadmin the database can be connected like this:

![Connect to PGdatabase](./media/pgdb1.png)

![Connect to PGdatabase](./media/pgdb2.png)

In the connection tab the following credentials have to be entered:

Username: root  
Password: root

![Connect to PGdatabase](./media/pgdb3.png)

Now the three tables that were created by the pipeline should there:  
![Connect to PGdatabase](./media/pgdb4.png)

The data can now be freely explored.

### Kestra

Access Kestra on https://localhost:8080

Login with the Username and the password you set in .env as KESTRA_USERNAME and KESTRA_PASSWORD

After logging into Kestra, you should see the `openparl_ingest_local` flow in the `deng` namespace. The flow file is automatically loaded on startup.

To run the pipleline:

1. Click on the flow `openparl_ingest_local`
2. Click "Execute"
3. Select the number of votes you want to process. The default is 100 votes.
4. Click "Execute" again to start

The pipeline runs three main tasks sequentially:

1. **ingest_votes**: This tasks fetches all votes from the Swiss Parliament API and loads them into PostgreSQL.
2. **ingest_voting**: This task festches all the individual voting records (from votes) and loads them into PostgreSQL.
3. **aggregate_party_summary**: The third task aggregates voting records into a per-party summary for each vote

Currently the flow is scheduled to run automatically every Monday morning at 6 AM. It supports backfills via the Kestra UI. You can see this when you have the flow `openparl_ingest_local` selected, under the Triggers tab.

![Architecture](./media/architecture.png)

## Instructions to start cloud pipeline

### Prerequisites

#### Google Cloud

Ensure that you have a working service account on the google cloud. The account needs permissions to create big query resources and storage buckets.
Save the credentials for the service account on you file system in a json file.
How this is done was covered in the course and will not be described here further.

#### Clone Repo

First clone this repository to be able to start the pipeline:
Navigate to the directory where you want to clone the repo and run the following command:  
`git clone https://github.com/hannah22700/DENG.git`

Navigate inside the repo:  
`cd DENG`

#### Env File and variables.tf

Ensure that you have a working .env file. For reference .env_example can be found in the repo. For an easy set up, copy it and rename it to .env.

The following .env variables are relevant for the cloud set up:

```
ENV_GOOGLE_CREDENTIALS
ENV_PROJECT_NAME
ENV_BUCKET_NAME
ENV_BIGQUERY_NAME
KESTRA_USERNAME
KESTRA_PASSWORD
KESTRA_POSTGRES_USERNAME
KESTRA_POSTGRES_PASSWORD
```

_Please specify the correct project name in the env file. This will be different for your set up_

If you change an env variable that is also used in variables.tf you have to change it there also.

Use the following table for reference which values need to be changed together.

| variable.tf       | .env                   |
| ----------------- | ---------------------- |
| `credentials`     | ENV_GOOGLE_CREDENTIALS |
| `project`         | ENV_PROJECT_NAME       |
| `bq_dataset_name` | ENV_BIGQUERY_NAME      |
| `gcs_bucket_name` | ENV_BUCKET_NAME        |

_Please make sure to configure the correct path for the credentials file and the correct project name!_

### Terraform

To be able to run the pipeline the google cloud resources have to be created with Terraform.

For this run the following commands (start out in the directory where you cloned this repo):

```bash
cd terraform
```

```bash
terraform plan
```

Review which resources terrafrom will create. It should create

- one storage bucket
- one big query dataset
- 3 google big query tables: votes, votings and partysummary

If everything looks correct run:

```bash
terraform apply
```

After again reviewing the changes terraform would like to make, enter yes into the prompt.

Check in google cloud if the ressources were created.
The big query tables should all be empty, but have a defined schema.

### Containers

Start the containers up with:
`docker compose up -d`

### Kestra

Access Kestra on https://localhost:8080

Login with the Username and the password you set in .env as KESTRA_USERNAME and KESTRA_PASSWORD

#### openparl_ingest_datalake

This Kestra flow ingests voting data from the Swiss Parliament API, processes it into CSV format, and uploads the results to Google Cloud Storage (GCS).

##### Tasks

| Task            | Description                                              |
| --------------- | -------------------------------------------------------- |
| `ingest_votes`  | Fetches vote metadata and uploads it to GCS.             |
| `votes_exist`   | Checks whether vote data exists before continuing.       |
| `ingest_voting` | Fetches detailed voting records and uploads them to GCS. |

##### Special Notes

- Runs in Docker using a custom Python image
- Uses `.pkl` files for task-to-task data sharing
- Supports manual date inputs (`since`, `until`)
- Scheduled to run weekly every Monday at 06:00
- Uses environment variables for GCP and credential configuration

##### Execution

1. Click on the flow `openparl_ingest_datalake`
2. Click "Execute"
3. Select the start and the end range of the votes that you want to process.
   - The time period has to include a range where the Notionalrat is in session, otherwise you cannot extract any votes. To check when the Nationalrat is in session you can use this website: https://www.parlament.ch/de/ratsbetrieb/sessionen
4. Click "Execute" again to start

#### openparl_ingest_bigquery

This Kestra flow downloads voting data files from Google Cloud Storage (GCS), stages them in BigQuery, transforms the data into analytics-ready tables, and creates aggregated party voting summaries.

##### Tasks

| Task                  | Description                                                               |
| --------------------- | ------------------------------------------------------------------------- |
| `stage_data`          | Downloads CSV files from GCS and loads them into BigQuery staging tables. |
| `transform_votes`     | Merges staged vote metadata into the `votes` table.                       |
| `transform_votings`   | Merges staged voting records into the `votings` table.                    |
| `drop_staging`        | Removes temporary staging tables after ingestion.                         |
| `create_partysummary` | Creates aggregated party-level voting summaries in BigQuery.              |

##### Special Notes

- Uses Docker-based Python execution with a custom image
- Uses BigQuery `MERGE` statements for incremental loading
- Automatically creates aggregated analytics tables
- Scheduled to run weekly every Monday at 08:00
- Uses environment variables for GCP, BigQuery, and credential configuration

##### Execution

1. Click on the flow `openparl_ingest_bigquery`
2. Click "Execute"
3. Select the date from which you want to ingest the data. This date references the cloud storage bucket files. So if you are running this on the same day as openparl_ingest_datalake you have to choose the date of that day.
4. Click "Execute" again to start

### Review Data

### Clean Up

After you are done with testing the pipeline, don't forget to destroy the terraform ressources again with

```bash
terraform destroy
```

Review the changes terraform would like to make and then answer the prompt with yes.

## Documentation

### Dependencies

The following python dependencies are in use:
| Package | Version | Explanation |
|-------------------|----------|-------------|
| click | 8.3.1 | used to add parameters to the main script through the command line |
| jupyter | 1.1.1 | used for jupyter notebooks to play around and test certain things |
| pandas | 3.0.1 | used for the organization of data into dataframes and some statistical methods |
| sqlalchemy | 2.0.48 | used for the engine to connect to the posgres DB|
| psycopg2-binary | 2.9.11 | Used to connect to the postgres DB|
| swissparlpy | 1.0.0 | used as abstraction of the SwissParl API |

### Extraction

The data extraction is done with the `dataconnector.py`

For the extraction of the data the python library swissparlpy is used.
The Library provides an abstraction to the api which makes it much easier to use.
See the github page of the library for more information: [SwissParlpy](https://github.com/metaodi/swissparlpy)

The dataconnector contains three methods:

| Method                        | Explanation                                                                                                                                                                                                 |
| ----------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| get_votes()                   | Is used to get all the occasions where there was a vote for a bill. Votes are only collected in German since the other languages offer only redundant data                                                  |
| get_voting(votes)             | gets the voting for each vote. A vote contains the person that voted, what they voted and with which party they are affiliated with.                                                                        |
| save_voting_of_vote(id, path) | helper method that gets the voting records of a single vote and saves it to the filesystem in the current directory to the foled voting. This is done to avoid a timeout when collecting the voting records |
| def delete_pickels(path)      | helper method to delete the saved pickles on the filesystem                                                                                                                                                 |

### Transformation

The data transformation is done with the `datatransform.py`

| Method                      | Explanation                                                                                                                                                                                   |
| --------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| clean_up_votes(votes)       | drops the unwanted column Language from the votes dataframe                                                                                                                                   |
| clean_up_voting(voting)     | drops the unwanted column Language and PargroupColor from the dataframe. It also reorganizes the indexes, since they are no longe correct after merging the votings together from the pickles |
| create_pary_summary(voting) | aggregates information about how every party voted on each bill, including summing up the total seats and calculating the mode for each voting Decision                                       |
| clean_column(name)          | helper method to remove spaces and special characters from dataframe column names                                                                                                             |

### Load

The loading of the data into the Postgres DB is done with the `main.py`
| Method | Explanation |
| ------ | ----------- |
|ingest_data(engine, data, target_table, chunksize) | converts a dataframe to sql and adds it to the DB |
| main(pg_user, pg_pass, pg_host, pg_port, pg_db, chunksize) | ties everything together, the loading the transforming and the ingestion of the data.|

### Pipeline Orchestration

The pipeline is orchestrated with [Kestra](https://kestra.io/). The flow definition can be found in `flows/openparl_ingest.yml`. It is loaded automatically into Kestra on startup via the `--flow-path` flag.

Some key design decisions:

- **Custom Docker image** (`openparl-kestra:latest`): All necessary Python dependencies are pre-installed to avoid re-installing them individually for every task.
- **pluginDefaults**: We share a base configuration for Docker task runner, container image, script files across all different tasks. This config is defined once under `pluginDefaults` and inherited by all tasks
- **Variables**: The database connection string and a predefined chunk size (100000) are defined as flow-level variables
- **Scheduling**: A weekly cron trigger runs the pipeline every Monday morning at 6 AM
- **Backfills**: The pipeline follows a full-refresh strategy: every run fetches the complete dataset and replaces the existing tables, making it idempotent. A single execution always produces a fully up-to-date database, regardless of missed runs. Backfills can be triggered manually through the Kestra UI under the Triggers tab.
