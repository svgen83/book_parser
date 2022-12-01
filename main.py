import os
import pathlib
import random
import requests

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlsplit, unquote

def make_directory(directory_name):
    pathlib.Path(directory_name).mkdir(parents=True, exist_ok=True)

def get_book_ids(start_number, fin_number,number_range ):
    return [str(random.randint(start_number, fin_number)) for i in range(number_range)]
    

def download_files(url, directory, id_book, book_name, ext):
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    file_name = os.path.join(directory, f"{id_book}_{book_name}.{ext}")
    with open(file_name, "wb") as file:
        file.write(response.content)


def parsing_html(id_book):
    url = f"https://tululu.org/b{id_book}/"
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find("h1")
    title = title_tag.text
    print(title)
    book_title, author = title.split("::")
    soup_link = soup.find('div', class_='bookimage').find('img')['src']
    image_link = urljoin(url, soup_link)
    print(image_link)
    comments = soup.find_all('span', class_='black')
    for comment in comments:
        print(comment.text)
    return sanitize_filename(book_title.strip()), image_link #,author.strip()


def check_for_redirect(response):
    if response.url  ==  "https://tululu.org/":
        raise requests.exceptions.HTTPError        


if __name__ == "__main__":

    
    make_directory("./books")
    make_directory("./books/covers")
    id_books = get_book_ids(9, 9, 1)
    for id_book in id_books:
        try:
            url = f"https://tululu.org/txt.php?id={id_book}"
            book_name, img_url = parsing_html(id_book)
            download_files(url, "./books", id_book, book_name,ext="txt")
            download_files(img_url, "./books/covers", id_book, book_name,ext="jpg")
        except requests.exceptions.HTTPError:
            print('Необходимый файл отсутствует')
        continue

    

###ссылка на книгу Пески Марса https://tululu.org/b32168
