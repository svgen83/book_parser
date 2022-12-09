# Book_parser

The program is designed for parsing pages and downloading books [on the library website] (https://tululu.org/).

## How to install

Python3 should already be installed.
Then use pip (or pip3 if there is a conflict with Python2) to install the dependencies:
```
pip install -r requirements.txt
```


## How to start

The program is launched from the command line. To run the program with the `cd` command, you first need to navigate to the folder containing the `main.py` file.
After that, on the command line, write:
```
python main.py 10, 20
```
In this case, the numbers `10, 20` can be any other positive integers. They indicate, respectively, the first and last position (id) of downloaded books.
It must be remembered that the second number must be greater than the first.

## Project Goals

The code was written for educational purposes in an online course for web developers [dvmn.org](https://dvmn.org/).
