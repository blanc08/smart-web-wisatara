import pandas as pd
import csv
import logging
import os
import requests
import xlsxwriter

# Web Scraping libraries
from bs4 import BeautifulSoup

from utils import make_output_dir

# Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ContentScrapper:
    def __init__(self, df: pd.DataFrame):
        # Prepare output dir in case not exist
        make_output_dir()

        self.df = df
        self.items = []
        self.csv_base_path = os.path.join(os.path.curdir, "out")

    def start_requests(self):
        for _, row in self.df.iterrows():
            self.parse(row)

    def parse(self, row: pd.Series):
        """
        Parse an items for given path name
        """

        soup = BeautifulSoup(requests.get(row["link"]).text, "html.parser")

        for content in soup.find_all("article", attrs={"class": "detail"}):
            merged = {**row, **{"content": content.prettify()}}
            self.items.append(merged)

        return self.items

    def save(self, filename="parsed.xlsx"):
        """
        docstring
        """
        max_header = {
            "index": 0,
            "length": 0,
        }

        for index, value in enumerate(self.items):
            length = len(value.keys())
            if length > max_header["length"]:
                max_header["length"] = length
                max_header["index"] = index

        # filepath
        workbook = xlsxwriter.Workbook(filename=filename)
        worksheet = workbook.add_worksheet()

        # Start from the first cell.
        # Rows and columns are zero indexed.
        row = 0
        column = 0

        # column = self.items[max_header["index"]].keys()

        # iterating through content list
        for dictionary in self.items:
            items = [value for value in dictionary.values()]
            for item in items:
                # write operation perform
                worksheet.write(row, column, str(item))
                column += 1

            column = 0
            # incrementing the value of row by one
            # with each iterations.
            row += 1

        workbook.close()


if __name__ == "__main__":
    df = pd.read_csv("./result.csv")

    parser = ContentScrapper(df=df)

    items = parser.start_requests()
    parser.save()
