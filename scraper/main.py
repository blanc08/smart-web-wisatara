import csv
import logging
import os
import requests

# Web Scraping libraries
from bs4 import BeautifulSoup

from utils import make_output_dir

# Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Scraper:
    def __init__(self, since: str):
        # Prepare output dir in case not exist
        make_output_dir()

        self.cursor = since
        self.items = []
        self.csv_base_path = os.path.join(os.path.curdir, "out")

    # TODO: Main method
    def parse(self, has_more=True):
        """
        Parse an items for given path name
        """

        page = 1

        pages = os.listdir(self.csv_base_path)

        if len(pages) > 0:
            pages = [
                (
                    int(str(page).split(".")[0])
                    if len(page.split(".")) > 1
                    else int(page)
                )
                for page in pages
            ]
            pages.sort(reverse=True)

            logger.info(f"current page {pages}")
            page = pages[0] + 1

        while has_more:
            has_more = self.parse_one(
                "https://www.detik.com/search/searchnews",
                params={
                    "query": "wisata",
                    "result_type": "latest",
                    "fromdatex": "01/01/2023",
                    "todatex": "27/06/2024",
                    "page": page,
                    "sortby": "time",
                },
            )
            page = page + 1

        return self.items

    def parse_one(self, url: str, params={}):
        """
        docstring
        """
        # fetch a page
        logger.info(f"Parsing items from path {url, params}")
        response = requests.get(url, params=params)

        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("article")

        if len(articles) == 0:
            return False

        for article in articles:
            thumbnail = article.find("img").attrs["src"]

            link_and_title = article.find("h3", attrs={"class": "media__title"})
            if link_and_title != None:
                title = link_and_title.text
                link = link_and_title.find("a")
                if link != None:
                    link = link.attrs["href"]

            date_div = article.find("div", attrs={"class": "media__date"})
            if date_div != None:
                date = date_div.find("span")
                if date != None:
                    date = date.attrs["d-time"]

            short = article.find("div", attrs={"class": "media__desc"})
            if short != None:
                short = short.text

            print(
                {
                    "title": title,
                    "link": link,
                    "date": date,
                    "thumbnail": thumbnail,
                    "short": short,
                }
            )
            self.items.append(
                {
                    "title": title,
                    "link": link,
                    "date": date,
                    "thumbnail": thumbnail,
                    "short": short,
                }
            )

        return True

    def save(self, file_name="result.csv"):
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

        with open(file_name, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            headers = self.items[max_header["index"]].keys()
            writer.writerow(headers)
            for row in self.items:
                writer.writerow([value for value in row.values()])


if __name__ == "__main__":

    parser = Scraper(since="today")

    items = parser.parse()
    parser.save()
    print(parser.items)
