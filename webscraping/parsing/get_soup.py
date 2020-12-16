import requests
from bs4 import BeautifulSoup

def get_soup(url) -> BeautifulSoup:
    response = requests.get(url)
    html = response.content
    return BeautifulSoup(html, 'html.parser')