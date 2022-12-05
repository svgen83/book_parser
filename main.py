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


def get_book_ids():
    parser = argparse.ArgumentParser(description="""
    Программа для парсинга библиотеки и скачивания книг""")
    parser.add_argument("start_id", type=int, help="id первой книги")
    parser.add_argument("fin_id", type=int, help="id последней книги")
    args = parser.parse_args()
    return [str(book_id) for book_id in range(args.start_id, args.fin_id + 1)]


def download_file(book_url, directory, book_id, book_name, ext):
    params = {"": "txt.php", "id": book_id}
    response = requests.get(book_url, params=params)
    response.raise_for_status()
    check_for_redirect(response)
    pathlib.Path(directory).mkdir(parents=True, exist_ok=True)
    save_file(response.content, "wb", directory, book_id, book_name, ext)


def get_response(book_id):
    url = f"https://tululu.org/b{book_id}/"
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    return response


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


def save_file(download_content,
              file_mode,
              directory,
              id_book,
              book_name,
              ext):
    file_name = os.path.join(directory,
                             f"{id_book}_{book_name}.{ext}")
    with open(file_name,
              file_mode) as file:
        file.write(download_content)


def main():
    book_ids = get_book_ids()
    base_path = "./books"

    for book_id in book_ids:
        try:
            book_path = os.path.join(base_path,
                                     book_id)

            book_url = "https://tululu.org/"
            response = get_response(book_id)
            parsed_page = parse_book_page(response)

            download_file(book_url,
                          book_path,
                          book_id,
                          parsed_page["book_title"],
                          ext="txt")
            download_file(parsed_page["image_link"],
                          book_path,
                          book_id,
                          parsed_page["book_title"],
                          ext="jpg")

            save_file(parsed_page["comments"],
                      "wt",
                      book_path,
                      book_id,
                      "Комментарии",
                      ext="txt")

            save_file(parsed_page["genres"],
                      "wt",
                      book_path,
                      book_id,
                      "Жанр",
                      ext="txt")

        except requests.exceptions.HTTPError:
            print("Необходимый файл отсутствует")
        except requests.exceptions.ConnectionError:
            time.sleep(1)
        continue


if __name__ == "__main__":
    main()
