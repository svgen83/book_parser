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

def get_response(page_number):
    responses = []
    url = f"https://tululu.org/l55/{str(page_number)}"
    response = requests.get(url)
    response.raise_for_status()
    print(response.url)
    check_for_redirect(response)
    return response


def parse_book_page(responses):
    all_urls = []
    for response in responses:
        soup = BeautifulSoup(response.text,
                         "lxml")
        parsed_objs = soup.find("body").find("div", id = "content").find_all(
    "table")
        id_urls = []
        for parsed_obj in parsed_objs:
            id_book = parsed_obj.find("a")["href"]
            id_url = urljoin(response.url, id_book)
            id_urls.append(id_url)
        all_urls.append(id_urls)
    print(all_urls)
    
    
def main():
    page_numbers = 10
    responses = []
    for page_number in range(page_numbers):  
        try:
            response = get_response(page_number)
            responses.append(response)
        except requests.exceptions.HTTPError:
            print("Необходимый файл отсутствует")
        except requests.exceptions.ConnectionError:
            time.sleep(1)
        continue    
    parse_book_page(responses)

if __name__ == "__main__":
    main()
