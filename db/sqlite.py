import sqlite3

import pandas
import pandas as pd
from IPython.core.display_functions import display


class DBSqlite:
    def __init__(self):
        self.conn = sqlite3.connect("news.db")
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        create_sql = """
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            date TEXT,
            link TEXT,
            content TEXT,
            publisher TEXT
        );
        """

        self.execute(create_sql)

    def execute(self, query):
        self.cur.execute(query)

    def execute(self, query, **args):
        self.cur.execute(query, args)


if __name__ == "__main__":
    db = DBSqlite()

    insert_qry = "INSERT INTO news (title, date, link, content, publisher) VALUES (?, ?, ?, ?, ?)"

    df = pd.read_csv("../finance.csv")
    # df.to_sql("news", db.conn, if_exists="append", index_label="id")
    df = pd.read_sql("SELECT * FROM news", db.conn, index_col="id")
    display(df)

    db.conn.commit()
    db.conn.close()
