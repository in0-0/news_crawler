import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By


class ParserYahoo:
    def __init__(self):
        pass

    def parse_articles_selenium(self, article_list):
        titles = article_list.find_elements(by=By.CLASS_NAME, value="sa_text")
        title_text = [
            t.find_element(by=By.CLASS_NAME, value="sa_text_title").text for t in titles
        ]
        links = [
            t.find_element(by=By.CLASS_NAME, value="sa_text_title").get_attribute(
                "href"
            )
            for t in titles
        ]
        articles = [self.get_article(l) for l in links]

        df = pd.DataFrame({"title": title_text, "link": links, "content": articles})
        return df

    def parse_articles_bs(self, link):
        req = requests.get(link)
        soup = BeautifulSoup(req.content, "html.parser")
        title_text = [t.text.strip("\n") for t in soup.find_all(class_="sa_text_title")]
        links = [t["href"] for t in soup.find_all(class_="sa_text_title")]
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

        date = soup.select_one(
            "#ct > div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div > span"
        )["data-date-time"]
        content = soup.select_one("article").text

        return {"date": date, "content": content}
