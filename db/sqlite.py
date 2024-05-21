import os
import sqlite3

import pandas
import pandas as pd
from IPython.core.display_functions import display


class DBSqlite:
    def __init__(self, path: str = "."):
        self.conn = sqlite3.connect(f"{path+os.sep}news.db")
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        create_sql = """
        CREATE TABLE IF NOT EXISTS news (
            title TEXT NOT NULL,
            date TEXT,
            link TEXT,
            content TEXT,
            publisher TEXT
        );
        """

        self.execute(create_sql)

    def insert_from_df(self, df):
        df.to_sql("news", self.conn, if_exists="append", index=False)
        self.conn.commit()

    def query_to_df(self, query: str = "SELECT * FROM news"):
        df = pd.read_sql(query, self.conn)

        return df

    def execute(self, query):
        self.cur.execute(query)

    def execute(self, query, **args):
        self.cur.execute(query, args)


if __name__ == "__main__":
    db = DBSqlite()

    insert_qry = "INSERT INTO news (title, date, link, content, publisher) VALUES (?, ?, ?, ?, ?)"

    # df.to_sql("news", db.conn, if_exists="append", index_label="id")
    df = pd.read_sql("SELECT * FROM news", db.conn, index_col="id")
    display(df)

    db.conn.commit()
    db.conn.close()
