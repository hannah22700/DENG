from sqlalchemy import create_engine
import dataconnector as dc
import click

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

    df = dc.get_votes()

    ingest_data(
        engine=engine,
        target_table=target_table,
        chunksize=chunksize,
        data = df
    )

if __name__ == "__main__":
    main()
