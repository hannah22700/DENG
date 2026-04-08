def ingest_data(
    engine,
    data,
    target_table: str,
    chunksize: int = 100000,
):

    data.head(0).to_sql(name=target_table, con=engine, if_exists="replace")

    data.to_sql(name=target_table, con=engine, if_exists="append", chunksize=chunksize)
