import argparse
import json
import logging
import os
import pathlib
import requests
import re
import time

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlparse

from pprint import pprint


logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


def check_for_redirect(response):
    if response.url == "https://tululu.org/":
        raise requests.exceptions.HTTPError
    

def parse_cmd():
    parser = argparse.ArgumentParser(description="""
    Программа для парсинга библиотеки и скачивания книг""")
    parser.add_argument(
        "-s",
        dest="start_page",
        default=1,
        type=int,
        help="номер страницы, с которой будет начиаться скачивание")
    parser.add_argument(
        "-f",
        dest="fin_page",
        default=1,
        type=int,
        help="номер страницы, которым будет завершаться скачивание")
    
    parser.add_argument(
        "-df", dest="dest_folder",
        type=str,default=".",
        help="путь к каталогам с результатами парсинга")

    parser.add_argument(
        "-si", "--skip_imgs",
        action='store_false',
        help="не скачивать картинки")

    parser.add_argument(
        "-st", "--skip_txt",
        action='store_false',
        help="не скачивать книги")

    parser.add_argument(
        "-j",dest="json_path",
        type=str, default="./books_description.json",
        help="путь к файлу с описанием книг")
    
    return parser.parse_args()


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
        parsed_objs = soup.select("#content .bookimage [href]")

        id_urls = [urljoin(response.url,
                            parsed_obj.get("href")
                           ) for parsed_obj in parsed_objs]
        all_urls.extend(id_urls)
        pprint(id_urls)
    return all_urls
    

def parse_book_page(response):
        
    soup = BeautifulSoup(response.text,
                         "lxml")
    title = soup.find("h1").text
    book_title, author = title.split("::")
    relativ_image_link = soup.select_one(".bookimage img").get("src")
    
    if soup.select_one("[href^='/txt.php']"):
        relativ_txt_link = soup.select_one(
            "[href^='/txt.php']").get("href")
    else: relativ_txt_link = '/ '
    
    txt_link = urljoin(response.url,
                       relativ_txt_link)
   
    image_link = urljoin(response.url,
                         relativ_image_link)

    comments_tags = soup.select(".texts")
    comments = [comments_tag.select_one("span.black").text
                for comments_tag in comments_tags]
    
    
    genres_tags = soup.select("span.d_book a")
    genres = [tag.text for tag in genres_tags]
    return {"txt_url": txt_link,
            "book_title": sanitize_filename(book_title.strip()),
            "image_link": image_link,
            "author": author.strip(),
            "comments": "\n".join(comments),
            "genres": "\n".join(genres)}


def download_file(file_url, directory, subdirectory,
                  book_id, book_name, ext):
    response = requests.get(file_url)
    response.raise_for_status()
    check_for_redirect(response)
    dir_path = os.path.join(directory, subdirectory)
    pathlib.Path(dir_path).mkdir(parents=True, exist_ok=True)
    filepath = os.path.join(dir_path,
                            f"{book_id}_{book_name}.{ext}")
    with open(filepath, "wb") as file:
        file.write(response.content)
            

def main():
    args = parse_cmd()
    responses = []
    books_description = []
    for page_number  in range(args.start_page, args.fin_page + 1):
        try:
            page_url = f"https://tululu.org/l55/{str(page_number)}"
            response = get_response(page_url)
            responses.append(response)
        except requests.exceptions.HTTPError:
            logger.info("Необходимый файл отсутствует")
        except requests.exceptions.ConnectionError:
            time.sleep(1)
        continue    
    book_urls = get_book_urls(responses)

    for book_url in book_urls:
        try:
            resp = get_response(book_url)
            book_description = parse_book_page(resp)
            
            parsed_book_url = urlparse(book_url)
            book_url_path = parsed_book_url.path
            book_id = book_url_path.replace('/','').replace('b','')

            if args.skip_txt:
                download_file(book_description["txt_url"],
                              args.dest_folder,
                              "books",
                              book_id,
                              book_description["book_title"],
                              ext = "txt")

            if args.skip_imgs:
                download_file(book_description["image_link"],
                              args.dest_folder,
                              "images",
                              book_id,
                              book_description["book_title"],
                              ext = "jpg")
            
            books_description.append(book_description)
        except requests.exceptions.HTTPError:
            logger.info("Необходимый файл отсутствует")
        except requests.exceptions.ConnectionError:
            time.sleep(1)
        continue
    books_description_json = json.dumps(books_description,
                                   ensure_ascii=False).encode('utf8')
    with open(args.json_path, "wb") as file:
        file.write(books_description_json)


if __name__ == "__main__":
    main()
