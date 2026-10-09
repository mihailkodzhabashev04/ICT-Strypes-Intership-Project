from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin

from .base import fetch_html



START_URL = 'https://quotes.toscrape.com/'
MAX_PAGES = 3
PAGE_DELAY = 0.5


def parse_page(html):
    """
    The logic is: Parse one page -> (records, link to next page ot None)
    """
    soup = BeautifulSoup(html, 'html.parser')

    records = []

    for card in soup.select('div.quote'):
        text = card.select_one("span.text")
        author = card.select_one("small.author")

        if text is None or author is None:
            continue

        tags = [tag.get_text(strip=True) for tag in card.select('div.tagsa.tag')]

        records.append({
            "quote": text.get_text(strip=True),
            "author": author.get_text(strip=True),
            "tags": ",".join(tags),
        })

    next_link = soup.select_one('li.next > a')
    if next_link is not None and next_link.get("href"):
        return records, next_link.get["href"]

    return records, None


def scrape_quotes():
    all_records = []
    url = START_URL

    for page_number in range(1, MAX_PAGES + 1):
        html = fetch_html(url)
        records, next_href = parse_page(html)

        if not records and page_number == 1:
            raise RuntimeError('No records found')

        all_records.extend(records)

        if next_href is None:
            break
        url = urljoin(START_URL, next_href)
        time.sleep(PAGE_DELAY)

    return all_records