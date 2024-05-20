from news_categories import sites

import pandas as pd
import time

from parser.naver import ParserNaver
from parser.yahoo import ParserYahoo

if __name__ == "__main__":
    parser = ParserNaver()

    for category, value in parser.category.items():
        cur_site = parser.base_url + value

        st = time.time()
        ret_dict = parser.parse_articles_bs(cur_site)
        et = time.time()
        print(f"parsing {category} done.. {et-st:.2f} seconds")
        df = pd.DataFrame(ret_dict)
        df["publisher"] = parser.name
        df.to_csv(f"{category}.csv", index=False)
        print(f"save {category} done..")
