import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from parser.defualt_parser import DefualtParser


class ParserYahoo(DefualtParser):
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

    def parse_articles(self, link, category):
        req = requests.get(link)
        soup = BeautifulSoup(req.content, "html.parser")
        titles = soup.find_all(class_=self.title_content)

        print(f"category: {category}, title cnt: {len(titles)}, link: {link}")

        return self.compose_elements(titles)

    def compose_elements(self, titles):
        title_text = [t.text for t in titles]
        links = [t.find("a")["href"] for t in titles]
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
            date = soup.find("time")["datetime"]
            content = "\n".join(
                [p.text for p in soup.find(class_=self.content_class).select("p")[:-1]]
            )
        except Exception as e:
            print(str(e) + ": " + link)
            return None
        return {"date": date, "content": content}
