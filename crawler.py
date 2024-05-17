from news_categories import sites

from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import re
import pandas as pd
import time
from bs4 import BeautifulSoup


def parse_articles(article_list):
    titles = article_list.find_elements(by=By.CLASS_NAME, value="sa_text")
    title_text = [
        t.find_element(by=By.CLASS_NAME, value="sa_text_title").text for t in titles
    ]
    links = [
        t.find_element(by=By.CLASS_NAME, value="sa_text_title").get_attribute("href")
        for t in titles
    ]
    articles = [get_article(l) for l in links]

    df = pd.DataFrame({"title": title_text, "link": links, "content": articles})
    return df


def parse_articles_bs(link):
    req = requests.get(link)
    soup = BeautifulSoup(req.content, "html.parser")
    title_text = [t.text.strip("\n") for t in soup.find_all(class_="sa_text_title")]
    links = [t["href"] for t in soup.find_all(class_="sa_text_title")]
    articles = [get_article(l) for l in links]

    df = pd.DataFrame({"title": title_text, "link": links, "content": articles})
    return df


def get_article(link: str):
    req = requests.get(link)
    soup = BeautifulSoup(req.content, "html.parser")
    ret = soup.select_one("article").text
    return ret


if __name__ == "__main__":
    for category, value in sites["naver"]["category"].items():
        cur_site = sites["naver"]["base_url"] + value

        st = time.time()
        parse_articles_bs(cur_site).to_csv(f"{category}.csv", index=False)
        et = time.time()
        print(f"{category} done.. {et-st:.2f} seconds")
