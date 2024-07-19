import polars as pl
import sqlite3
# import time

DB = "data.db" # placeholder name, please rename

class BME680Data():
    def __init__(
        self,
        database: str,
        query: str = None,
    ):
        if query is None: 
            query = "SELECT * FROM BME688"

        print(database)
        con = sqlite3.connect(database)
        
        df = self.read_from_db(query, con)

        self.con = con
        self.df = df
        self.query = query

    def read_from_db(self, query, con):
        return pl.read_database(
            query,
            con,
        ).with_columns(
            (pl.col("time") * 1000).cast(pl.Datetime(time_unit='ms'))
        )

    def update(self, query = None) -> pl.DataFrame:
        if query is None:
            query = self.query

        con = self.con

        df = self.read_from_db(query, con)

        self.df = df
        
        return df