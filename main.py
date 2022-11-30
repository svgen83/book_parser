import os
import pathlib
import random
import requests



def make_directory(directory_name):
    pathlib.Path(directory_name).mkdir(parents=True, exist_ok=True)
    

def download_files(directory_name):
    random.randint(10000, 99999)
    id_books = [str(random.randint(10000, 99999)) for i in range(9)]
    for id_book in id_books:
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
    print(response.url)
    print(response.status_code)
    print(response.history)
        


if __name__ == "__main__":

    directory_name = "./books"
    make_directory(directory_name)
    try:
        download_files(directory_name)
    except requests.exceptions.HTTPError:
        print('Необходимый файл отсутствует')
    



###ссылка на книгу Пески Марса https://tululu.org/txt.php?id=32168
