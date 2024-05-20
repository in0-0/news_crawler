from abc import ABC, abstractmethod


@ABC
class AbcParser:
    def __init__(self):
        pass

    @abstractmethod
    def parse_articles(self, link: str):
        pass

    @abstractmethod
    def get_article(self, link: str):
        pass
