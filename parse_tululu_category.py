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

def get_response(url):
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    return response


def get_book_urls(responses):
    all_urls = []
    for response in responses:
        soup = BeautifulSoup(response.text,
                         "lxml")
        parsed_objs = soup.find("body").find("div", id = "content").find_all(
    "table")
        id_urls = [
                    urljoin(response.url,
                            parsed_obj.find("a")["href"]) for parsed_obj in parsed_objs
                  ]
        all_urls.extend(id_urls)
    return all_urls
    

def parse_book_page(response):
    soup = BeautifulSoup(response.text,
                         "lxml")
    title = soup.find("h1").text
    book_title, author = title.split("::")
    relativ_image_link = soup.find("div",
                                   class_="bookimage").find("img")["src"]
    image_link = urljoin(response.url,
                         relativ_image_link)

    comments_tags = soup.find_all("div", class_="texts")
    comments = [comments_tag.find("span", class_="black").text
                for comments_tag in comments_tags]

    genres_tags = soup.find("span", class_="d_book").find_all("a")
    genres = [tag.text for tag in genres_tags]
    return {"book_title": sanitize_filename(book_title.strip()),
            "image_link": image_link,
            "author": author.strip(),
            "comments": "\n".join(comments),
            "genres": "\n".join(genres)}
            

def main():
    page_numbers = 10
    responses = []
    for page_number in range(page_numbers):  
        try:
            page_url = f"https://tululu.org/l55/{str(page_number)}"
            response = get_response(page_url)
            responses.append(response)
        except requests.exceptions.HTTPError:
            print("Необходимый файл отсутствует")
        except requests.exceptions.ConnectionError:
            time.sleep(1)
        continue    
    book_urls = get_book_urls(responses)
    print(book_urls)
    for book_url in book_urls:
        try:
            resp = get_response(book_url)
            book_info = [parse_book_page(resp)]
        except requests.exceptions.HTTPError:
            print("Необходимый файл отсутствует")
        except requests.exceptions.ConnectionError:
            time.sleep(1)
        continue
    print (book_info)
            
    

if __name__ == "__main__":
    main()
