"""
In this file are shared helpers for both scrapers.

fetch_html - the function that makes HTTP requests

ScraperError - the exception scrapers raise.
"""

import requests

HEADERS = {'User-Agent': 'Mozilla/5.0'}
REQUEST_TIMEOUT = 10


def fetch_html(url):
    """
    Download the page and return its HTML text.
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise RuntimeError('Request timed out.')
    except requests.exceptions.ConnectionError:
        raise RuntimeError('Connection error.')
    except requests.exceptions.HTTPError:
        raise RuntimeError(f'HTTP error.')
    except requests.exceptions.RequestException:
        raise RuntimeError('Request failed')

    response.encoding = 'utf-8'
    return response.text