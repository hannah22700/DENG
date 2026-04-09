import os

import click
import pandas as pd
from sqlalchemy import create_engine

import scripts.dataconnector as dc
import scripts.dataingest as di
import scripts.datatransform as dt


@click.command()
@click.option("--pg-user", default="root", help="PostgreSQL username")
@click.option("--pg-pass", default="root", help="PostgreSQL password")
@click.option("--pg-host", default="localhost", help="PostgreSQL host")
@click.option("--pg-port", default="5432", help="PostgreSQL port")
@click.option("--pg-db", default="openparl", help="PostgreSQL database name")
@click.option("--chunksize", default=100000, type=int, help="Chunk size for ingestion")
@click.option("--voteCount", default=100, type=int, help="Number of votes to get votings for")
def main(pg_user, pg_pass, pg_host, pg_port, pg_db, chunksize, votecount):
    print("Starting Pipeline")
    engine = create_engine(
        f"postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}"
    )

    __location__ = os.path.realpath(os.getcwd())
    path = os.path.join(__location__, "voting")

    print("Getting votes...")
    votes = dc.get_votes()

    dfvotes = pd.DataFrame(votes)
    dfvotes = dt.clean_up_votes(dfvotes)

    di.ingest_data(
        engine=engine, target_table="votes", chunksize=chunksize, data=dfvotes
    )

    print("Finished Ingesting Votes")

    print("Gettting vortings")
    dfvoting = dc.get_voting_of_votes(votes[:votecount], path)
    dfvoting = dt.clean_up_voting(dfvoting)

    di.ingest_data(
        engine=engine, target_table="voting", chunksize=chunksize, data=dfvoting
    )

    print("Finished Ingesting Votings")

    print("Creating Party summary")

    dfpartysummary = dt.create_party_summary(dfvoting)

    di.ingest_data(
        engine=engine,
        target_table="partysummary",
        chunksize=chunksize,
        data=dfpartysummary,
    )

    print("Finished Ingesting Party Summary")


if __name__ == "__main__":
    main()
