from bs4 import BeautifulSoup
import requests
from .table import Table


class Page:
    def __init__(self, url: str, headers: dict = {}) -> None:
        self.url = url
        self.headers = headers

    def fetch(self) -> BeautifulSoup:
        page = requests.get(self.url).text
        self.soup = BeautifulSoup(page, "html.parser")
        return self.soup

    def generate_tables(self) -> Table:
        tables = self.soup.find_all("table")
        tables = [Table(table) for table in tables]
        self.tables = tables
        return self.tables

    def get_tables(self) -> list:
        """returns list of Table class"""
        self.fetch()
        return self.generate_tables()
