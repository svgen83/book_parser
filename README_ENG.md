# Book_parser

The program is intended for parsing pages and downloading books of the "Science Fiction" genre [on the library's website] (https://tululu.org/).

## How to install

Python3 should already be installed.
Then use pip (or pip3 if there is a conflict with Python2) to install the dependencies:
```
pip install -r requirements.txt
```


## How to start

The program is launched from the command line. To run the program with the `cd` command, you first need to navigate to the folder containing the `parse_tululu_category.py` file.
After that, on the command line, write:
```
python parse_tululu_category.py
```
To set the values of downloaded books, after calling the program on the command line, enter the numbers of the first and last pages from which the download occurs, in the following form:
`-s=n` and `-f=n`, where `n` is a positive integer. It must be remembered that the second number must be greater than the first.
By default, the first and last pages of books are set to `1` and `4`.

## Additional settings
If the user does not consider it necessary to download book covers or text files with books, then additional flags should be added on the command line:
`-si` or `--skip_image` to skip downloading cover images;
`-st` or `--skip_text` to skip downloading files with book text.
Files with text and images are downloaded respectively to the "books" and "images" folders, which are created by default in the directory with the program. The file with the description of the downloaded books in the .json format will also be located by default in the directory with the program.
The general folder download location can be changed by "books" and "images" by specifying the path using the `-df` option.
Similarly, you can change the location of the book description file by specifying the path using the `-j` parameter.


## Project Goals

The code was written for educational purposes in an online course for web developers [dvmn.org](https://dvmn.org/).
