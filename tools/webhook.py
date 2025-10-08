import requests
from bs4 import BeautifulSoup

def get_site_html(url: str) -> BeautifulSoup:
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Site '{url}' could not be reached")

    return BeautifulSoup(response.text, "html.parser")