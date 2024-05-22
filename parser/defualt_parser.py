from abc import ABC, abstractmethod


class DefualtParser:
    request_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0",
        "Referer": "",
    }

    def __init__(self):
        pass

    def parse_articles(self, link: str, category: str):
        print("Not implemented!")

    def get_article(self, link: str):
        print("Not implemented!")
