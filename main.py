import os
import pathlib
import random
import requests



def make_directory(directory_name):
    pathlib.Path(directory_name).mkdir(parents=True, exist_ok=True)

def get_book_ids(start_number, fin_number,number_range ):
    return [str(random.randint(start_number, fin_number)) for i in range(number_range)]
    

def download_files(directory_name, id_book):
    url = f"https://tululu.org/txt.php?id={id_book}"
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    book_name = f"{directory_name}/book_{id_book}.txt"
    with open(book_name, "wb") as file:
        file.write(response.content)


def check_for_redirect(response):
    if response.url  ==  "https://tululu.org/":
        raise requests.exceptions.HTTPError        


if __name__ == "__main__":

    directory_name = "./books"
    make_directory(directory_name)
    id_books = get_book_ids(10000, 50000, 10)
    for id_book in id_books:
        try:
            download_files(directory_name, id_book)
        except requests.exceptions.HTTPError:
            print('Необходимый файл отсутствует')
        continue

    



###ссылка на книгу Пески Марса https://tululu.org/txt.php?id=32168
