from sqlalchemy import create_engine
import dataconnector as dc
import datatransform as dt
import click
import pandas as pd
import os

def ingest_data(        
        engine,
        data,
        target_table: str,
        chunksize: int = 100000,):
    
    data.head(0).to_sql(        
        name=target_table,
        con=engine,
        if_exists="replace")

    data.to_sql(
        name=target_table,
        con=engine,
        if_exists="append",
        chunksize = chunksize
    )



@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL username')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default='5432', help='PostgreSQL port')
@click.option('--pg-db', default='openparl', help='PostgreSQL database name')
@click.option('--chunksize', default=100000, type=int, help='Chunk size for ingestion')
@click.option('--target-table', default='votes', help='Target table name')
def main(pg_user, pg_pass, pg_host, pg_port, pg_db, chunksize, target_table):
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')
    __location__ = os.path.realpath(os.getcwd())
    path = os.path.join(__location__, "voting")

    votes = dc.get_votes()

    dfvotes = pd.DataFrame(votes)
    dfvotes = dt.clean_up_votes(dfvotes)

    ingest_data(
        engine=engine,
        target_table='votes',
        chunksize=chunksize,
        data = dfvotes
    )

    print("Finished Ingesting Votes")

    dfvoting = dc.get_voting_of_votes(votes[:50], path)
    dfvoting = dt.clean_up_voting(dfvoting)

    ingest_data(
        engine=engine,
        target_table='voting',
        chunksize=chunksize,
        data = dfvoting
    )

    print("Finished Ingesting Votings")

    dfpartysummary = dt.create_pary_summary(dfvoting)

    ingest_data(
        engine=engine,
        target_table='partysummary',
        chunksize=chunksize,
        data = dfpartysummary
    )

    print("Finished Ingesting Party Summary")

if __name__ == "__main__":
    main()
