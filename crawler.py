from db.sqlite import DBSqlite
from news_categories import sites

import pandas as pd
import time

from parser.naver import ParserNaver
from parser.parser_factory import PB_YAHOO, PB_NAVER, ParserFactory
from parser.yahoo import ParserYahoo

if __name__ == "__main__":
    publishers = [PB_YAHOO, PB_NAVER]
    db = DBSqlite()

    # for publisher in publishers:
    #     parser = ParserFactory.get_parser(publisher)
    #
    #     for category, value in parser.category.items():
    #         cur_site = parser.base_url + value
    #
    #         st = time.time()
    #         ret_dict = parser.parse_articles(cur_site)
    #         et = time.time()
    #         print(f"parsing {category} done.. {et-st:.2f} seconds")
    #         df = pd.DataFrame(ret_dict)
    #         df = df.dropna()
    #         df["publisher"] = parser.name
    #         # df.to_csv(f"{category}.csv", index=False)
    #
    #         db.insert_from_df(df)
    #         print(f"save {category} to DB done..")
    #
    #         time.sleep(2)

    df = db.query_to_df()
    df.to_csv("news_db.csv", index=False)
