import os
import pathlib
import random
import requests

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlsplit, unquote



def get_book_ids(start_number, fin_number,number_range):
    return [str(random.randint(start_number, fin_number)) for i in range(number_range)]
    

def download_files(book_url, directory, id_book, book_name, ext):
    response = requests.get(book_url)
    response.raise_for_status()
    check_for_redirect(response)
    save_file(response.content,"wb", directory, id_book, book_name, ext)


def save_file(download_content,file_mode,
              directory, id_book, book_name, ext):
    file_name = os.path.join(directory, f"{id_book}_{book_name}.{ext}")
    with open(file_name, file_mode) as file:
        file.write(download_content)


def parsing_book_page(book_id):
    url = f"https://tululu.org/b{book_id}/"
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    soup = BeautifulSoup(response.text, 'lxml')
    title = soup.find("h1").text
    book_title, author = title.split("::")
    relativ_image_link = soup.find('div', class_='bookimage').find('img')['src']
    image_link = urljoin(url, relativ_image_link)
    comments_tags = soup.find_all('div', class_='texts')
    comments = []
    for comments_tag in comments_tags:
        comment = comments_tag.find('span', class_='black').text
        comments.append(comment)
##        file_name = os.path.join("./books/comments", f"{id_book}.txt")
##        with open(file_name, "ta") as file:
##            file.write(f"{comment_text}\n")
    genres_tags = soup.find('span', class_='d_book').find_all("a")
    print(genres_tags)
    genres = []
    for tag in genres_tags:
        genre = tag.text
        genres.append(genre)
##        file_name = os.path.join("./books/genres", f"{id_book}.txt")
##        with open(file_name, "wt") as file:
##            file.write(genre.text)
    return {"book_title": sanitize_filename(book_title.strip()),
            "image_link": image_link,
            "author": author.strip(),
            "comments": "\n".join(comments),
            "genres": "\n".join(genres)}


def main():
 
    book_ids = get_book_ids(9, 9, 1)
    base_directory = "./books"
    
    for book_id in book_ids:
        try:
            book_dir = os.path.join(base_directory, book_id)
            pathlib.Path(book_dir).mkdir(parents=True, exist_ok=True)
            
            book_url = f"https://tululu.org/txt.php?id={book_id}"
            parsed_page = parsing_book_page(book_id)
            
            download_files(book_url, book_dir, book_id,
                           parsed_page["book_title"],
                           ext="txt")
            download_files(parsed_page["image_link"],
                           book_dir, book_id,
                           parsed_page["book_title"],ext="jpg")
            print(parsed_page["comments"])
            save_file(parsed_page["comments"],"wt",
                      book_dir, book_id,
                      "комментарии",
                      ext="txt")
            save_file(parsed_page["genres"],"wt",
                      book_dir, book_id,
                      "Жанр",
                      ext="txt")
        except requests.exceptions.HTTPError:
            print('Необходимый файл отсутствует')
        continue




def check_for_redirect(response):
    if response.url  ==  "https://tululu.org/":
        raise requests.exceptions.HTTPError        


if __name__ == "__main__":
    main()

    

    

###ссылка на книгу Пески Марса https://tululu.org/b32168
