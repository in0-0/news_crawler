import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from parser.parser import AbcParser


class ParserYahoo(AbcParser):
    def __init__(self):
        self.name = "yahoo"
        self.base_url = "https://finance.yahoo.com/topic/"
        self.category = {
            "economics": "economic-news",
            "tech": "tech",
            "housing": "housing-market",
        }

        self.title_content = "Mb(5px)"
        self.date_selector = "time"
        self.content_class = "caas-body"

    def parse_articles(self, link):
        req = requests.get(link)
        soup = BeautifulSoup(req.content, "html.parser")
        titles = soup.find_all(class_=self.title_content)
        title_text = [t.text for t in titles]
        links = [t.find("a")["href"] for t in titles]
        articles = [self.get_article(l) for l in links]

        ret_dict = {
            "title": title_text,
            "date": [a["date"] for a in articles],
            "link": links,
            "content": [a["content"] for a in articles],
        }
        return ret_dict

    def get_article(self, link: str):
        req = requests.get(link)
        soup = BeautifulSoup(req.content, "html.parser")
        date = soup.find("time")["datetime"]
        content = "\n".join(
            [p.text for p in soup.find(class_=self.content_class).select("p")[:-1]]
        )
        return {"date": date, "content": content}
