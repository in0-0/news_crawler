import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from parser.defualt_parser import DefualtParser


class ParserCNBC(DefualtParser):
    def __init__(self):
        self.name = "cnbc"
        self.base_url = "https://www.cnbc.com/"
        self.category = {
            "economy": "economy",
            "finance": "finance",
            "real_estate": "real-estate",
            "industry": "industrials",
            "small_business": "small-business",
            "enterprise": "enterprise",
        }

        self.card_container = "Card-titleContainer"
        self.premium_content = "InvestingClubPill-investingClubPillLink"
        self.title_content = "Card-title"
        self.date_selector = "time"
        self.content_class_free = "group"
        self.content_class_premium = "xyz-data"

    def parse_articles(self, link, category):
        req = requests.get(link)
        soup = BeautifulSoup(req.content, "html.parser")
        titles = soup.find_all(class_=self.card_container)

        print(f"category: {category}, title cnt: {len(titles)}, link: {link}")

        return self.compose_elements(titles)

    def compose_elements(self, titles):
        title_text = [
            t.find(class_=self.title_content).text
            for t in titles
            if t.find(class_=self.premium_content) is None
        ]
        links = [
            t.find(class_=self.title_content)["href"]
            for t in titles
            if t.find(class_=self.premium_content) is None
        ]
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
        print(link)
        try:
            req = requests.get(link, headers=self.request_headers)
            soup = BeautifulSoup(req.content, "html.parser")
            date = soup.find("time")["datetime"]
            content = (
                "\n".join(
                    [g.text for g in soup.find_all(class_=self.content_class_free)]
                )
                if soup.find(class_=self.content_class_premium) is None
                else soup.find(class_=self.content_class_premium).text
            )
            print(content)

        except Exception as e:
            print(str(e) + link)
            return None
        return {"date": date, "content": content}
