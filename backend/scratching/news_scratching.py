"""
Scratching news.
"""

import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import re

load_dotenv()
API_ID = os.getenv("API_ID_NEWS")
API_HASH = os.getenv("API_HASH_NEWS")


regions = {
    "Київ": 'https://www.ukr.net/news/kyiv.html',
    "Львів": "https://www.ukr.net/news/lviv.html",
    "Одеса": "https://www.ukr.net/news/odesa.html",
    "Дніпро": 'https://www.ukr.net/news/dnipro.html',
    "Харків": "https://www.ukr.net/news/kharkiv.html",
    "Запоріжжя": "https://www.ukr.net/news/zaporizhzhya.html",
    "Черкаси": "https://www.ukr.net/news/cherkasy.html",
    "Полтава": "https://www.ukr.net/news/poltava.html",
    "Вінниця": "https://www.ukr.net/news/vinnytsya.html",
    "Житомир": "https://www.ukr.net/news/zhytomyr.html",
    "Суми": "https://www.ukr.net/news/sumy.html",
    "Чернігів": "https://www.ukr.net/news/chernihiv.html",
    "Хмельницький": "https://www.ukr.net/news/hmelnitskiy.html",
    "Івано-Франківськ": "https://www.ukr.net/news/ivano_frankivsk.html",
    "Тернопіль": "https://www.ukr.net/news/ternopil.html",
    "Рівне": "https://www.ukr.net/news/rivne.html",
    "Кропивницький": "https://www.ukr.net/news/kropivnitskiy.html",
    "Миколаїв": "https://www.ukr.net/news/mikolayiv.html",
    "Луцьк": "https://www.ukr.net/news/lutsk.html",
    "Херсон": "https://www.ukr.net/news/kherson.html",
    "Чернівці": "https://www.ukr.net/news/chernivtsi.html",
    "Ужгород": "https://www.ukr.net/news/uzhgorod.html",
    "Луганськ": "https://www.ukr.net/news/luhansk.html",
    "Донецьк": "https://www.ukr.net/news/donetsk.html",
    "Крим": "https://www.ukr.net/news/crimea.html"
}

all_news = {}

def get_news():
    """
    Scrapes the latest news headlines and links for each region specified 
    in the 'regions' dictionary from the ukr.net website.

    It iterates through each region and its URL, sends an HTTP GET request, parses the HTML response
    using BeautifulSoup, and extracts the titles and links of the top 5 news articles.
    News titles containing Russian characters are skipped.
    The extracted news for each region are then stored in the 'all_news' dictionary with the region
    name as the key and the top 5 news items (title::link) joined by '///' as the value.

    Returns:
        dict[str, str]: A dictionary where keys are Ukrainian region names and values are strings
                       containing the top 5 news headlines and their links, separated by '///'.
                       Each news item is formatted as "title::link".
    """
    for region_name, region_url in regions.items():
        response = requests.get(region_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        news_items = soup.find_all('div', class_='im-tl')

        region_news = []
        for item in news_items:
            a_tag = item.find('a')
            if a_tag:
                title = a_tag.get_text(strip=True)
                link = a_tag['href']
                if re.search(r"[ёЁыЫэЭъЪ]", title) is not None:
                    continue
                region_news.append(f"{title}::{link}")

        all_news[region_name] = "///".join(region_news[:5])

    return all_news
