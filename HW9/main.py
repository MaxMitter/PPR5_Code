from bs4 import BeautifulSoup
import requests

def getSiteContent(url: string):
    if "https://github.com" not in url or "https://www.github.com" not in url:
        raise ValueError(f"{url} is not a valid GitHub URL")

    content = BeautifulSoup(requests.get(url).text, "html.parser")
