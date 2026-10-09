"""
A scraper for https://books.toscrape.com/

Extracted data (each record is a dictionary)
    title (book title),
    price (prices like £51.77),
    availability (In stock ot not),
    rating (from 1 tp 5)
    category (for example Philosophy)
"""



from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin

from .base import fetch_html


BASE_URL = 'https://books.toscrape.com/'


MAX_CATEGORIES = 10 #First N categories from the menu
BOOKS_PER_CATEGORY = 5 #Books taken from each category
PAGE_DELAY = 0.5 #Pause between rquests

#The site stores the ratings as a CSS class
RATING_WORDS = {"One":1, "Two":2, "Three":3, "Four":4, "Five":5}

def parse_categories(html):
    #Return a list of (name, relative_link) from the category menu.
    soup = BeautifulSoup(html, 'html.parser')
    categories = []

    #The nested <ul> holds the categories, outer <li> is "Books" (all)
    for link in soup.select('div.side_categories ul li ul li a'):
        name = link.get_text(strip=True)
        href = link.get('href')
        if name and href:
            categories.append((name, href))

    return categories

def parse_books(html, category):
    """
    Parses one page of books and returns a list of dictionaries.

    Books with missing attributes are skipped.
    """
    soup = BeautifulSoup(html, 'html.parser')
    records = []

    for card in soup.select('article.product_pod'):
        link = card.select_one('h3 a')
        price = card.select_one('p.price_color')
        rating_tag = card.select_one("p.star-rating")
        stock = card.select_one('p.availability')

        if link is None or price is None:
            continue

        rating = None
        if rating_tag is not None:
            for css_class in rating_tag.get("class", []):
                if css_class in RATING_WORDS:
                    rating = RATING_WORDS[css_class]

        records.append(
            {
                "title": link.get('title') or link.get_text(strip=True),
                "price": price.get_text(strip=True),
                "availability": stock.get_text(strip=True) if stock else "",
                "rating": rating,
                "category": category
            }
        )

    return records

def scrape_books():
    #Scrape books from several categories and return a list of records.
    home_html = fetch_html(BASE_URL)
    categories = parse_categories(home_html)

    if not categories:
        raise RuntimeError('No categories found')

    records = []
    for name, href in categories[:MAX_CATEGORIES]:
        time.sleep(PAGE_DELAY)
        category_html = fetch_html(urljoin(BASE_URL, href))
        records.extend(parse_books(category_html, name)[:BOOKS_PER_CATEGORY])

    return records