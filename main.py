import os
import requests
from bs4 import BeautifulSoup
import re
import subprocess

from steamDownloader import download_mod
from steamDownloader import is_collection

if __name__ == "__main__":
    urlgame = input("Введите ссылку на модификацию или коллекцию: ")
    response = requests.get(urlgame)
    html_content = response.text

    if not is_collection(html_content):
        print("Это коллекция!")
        # todo сделать в след. обновлениях!
        pass
    else:
        download_mod(urlgame)
