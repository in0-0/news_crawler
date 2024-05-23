import time

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from parser.defualt_parser import DefualtParser


class ParserNaver(DefualtParser):

    def __init__(self):
        self.name = "naver"
        self.base_url = "https://news.naver.com/breakingnews/section/101/"
        self.category = {
            "finance": "259",
            "stock": "258",
            "industry": "261",
            "venture": "771",
            "real_estate": "260",
            "global": "262",
        }

        self.title_content = "sa_text_title"
        self.date_selector = "#ct > div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div > span"
        self.content_class = "article"

    def parse_articles(self, link, category):
        req = requests.get(link, headers=self.request_headers)
        soup = BeautifulSoup(req.content, "html.parser")
        titles = soup.find_all(class_=self.title_content)

        print(f"category: {category}, title cnt: {len(titles)}, link: {link}")

        return self.compose_elements(titles)

    def compose_elements(self, titles):
        title_text = [t.text for t in titles]
        links = [t["href"] for t in titles]
        articles = [self.get_article(l) for l in links]
        dates = [a["date"] if a is not None else "9999-12-31" for a in articles]
        contents = [a["content"] if a is not None else "None" for a in articles]
        ret_dict = {
            "title": title_text,
            "date": dates,
            "link": links,
            "content": contents,
        }
        return ret_dict

    def get_article(self, link: str):
        try:
            req = requests.get(link, headers=self.request_headers)
            soup = BeautifulSoup(req.content, "html.parser")

            date = soup.select_one(self.date_selector)["data-date-time"]
            content = soup.select_one(self.content_class).text

            time.sleep(2)
        except Exception as e:
            print(str(e) + ": " + link)
            return None

        return {"date": date, "content": content}
