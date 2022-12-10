import argparse
import os
import pathlib
import requests
import time

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin


def check_for_redirect(response):
    if response.url == "https://tululu.org/":
        raise requests.exceptions.HTTPError

def get_response():
    url = "https://tululu.org/l55/"
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    return response


def parse_book_page(response):
    url = "https://tululu.org/l55/"
    soup = BeautifulSoup(response.text,
                         "lxml")
    parsed_objects = soup.find("body").find("div", id = "content").find_all(
    "table")
    for parsed_object in parsed_objects:
        id_book = parsed_object.find("a")["href"]
        id_url = urljoin(url, id_book)
        print(id_url)
    
    

def main():
    response = get_response()
    
    parse_book_page(response)


if __name__ == "__main__":
    main()
