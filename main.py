import requests




def download_file(file_name):
    url = "https://tululu.org/txt.php?id=32168"
    response = requests.get(url)
    response.raise_for_status()
    with open(file_name, "wb") as file:
        file.write(response.content)


if __name__ == "__main__":

    download_file("book.txt")





