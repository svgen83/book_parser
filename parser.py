import requests

from bs4 import BeautifulSoup


url = "https://tululu.org/b1/"
#'https://www.franksonnenbergonline.com/blog/are-you-grateful/'
response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'lxml')

#soup.get_text()
title_tag = soup.find("h1")
title = title_tag.text
book_name, author = title.split("::")
print(book_name.strip())
print(author.strip())
