"""
scripts/scrape.py
Scrapes floral ethnic dress listings from Myntra.

Usage:
    python scripts/scrape.py --pages 10 --output data/raw/myntra_raw.csv

Note: Run responsibly. Add delays between requests. Check Myntra's
      robots.txt and terms of service before scraping in production.
"""

import argparse
import csv
import os
import time
import random
import logging
from datetime import datetime
from typing import List, Dict

import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

BASE_URL = "https://www.myntra.com/ethnic-dresses"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/123.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-IN,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml",
}

FIELDNAMES = [
    "id", "brand", "title", "price", "mrp", "discount_pct",
    "dress_shape", "sleeve_length", "hemline", "neck_style",
    "dress_length", "fabric", "slit_detail", "pattern",
    "sizes_available", "rating", "rating_count", "url", "scraped_at",
]


def get_listings(page: int = 1) -> List[Dict]:
    """Fetch one page of search results and return a list of raw listing dicts."""
    url = f"{BASE_URL}?p={page}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        log.error(f"Request failed for page {page}: {e}")
        return []

    soup = BeautifulSoup(resp.text, "lxml")
    listings = []

    for card in soup.select(".product-base"):
        try:
            listings.append({
                "brand":        card.select_one(".product-brand").get_text(strip=True),
                "title":        card.select_one(".product-product").get_text(strip=True),
                "price":        _parse_price(card.select_one(".product-discountedPrice")),
                "mrp":          _parse_price(card.select_one(".product-strike")),
                "url":          "https://www.myntra.com" + card.select_one("a")["href"],
                "scraped_at":   datetime.utcnow().isoformat(),
            })
        except (AttributeError, TypeError):
            continue

    log.info(f"Page {page}: {len(listings)} listings found")
    return listings


def get_product_detail(url: str) -> Dict:
    """Fetch a product page and extract design attributes."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        log.warning(f"Could not fetch {url}: {e}")
        return {}

    soup = BeautifulSoup(resp.text, "lxml")
    detail = {}

    for row in soup.select(".index-row"):
        key_el = row.select_one(".index-rowKey")
        val_el = row.select_one(".index-rowValue")
        if key_el and val_el:
            k = key_el.get_text(strip=True).lower().replace(" ", "_")
            detail[k] = val_el.get_text(strip=True)

    return detail


def _parse_price(el) -> int:
    if el is None:
        return 0
    text = el.get_text(strip=True).replace("₹", "").replace(",", "").strip()
    try:
        return int(text)
    except ValueError:
        return 0


def scrape(pages: int = 10, output: str = "data/raw/myntra_raw.csv", delay: float = 1.5):
    os.makedirs(os.path.dirname(output), exist_ok=True)
    all_rows = []

    for page in range(1, pages + 1):
        listings = get_listings(page)
        for item in listings:
            time.sleep(random.uniform(0.5, delay))
            detail = get_product_detail(item.get("url", ""))
            item.update(detail)
            all_rows.append(item)

        time.sleep(random.uniform(delay, delay * 2))

    with open(output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(all_rows)

    log.info(f"Saved {len(all_rows)} listings → {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pages",  type=int, default=10)
    parser.add_argument("--output", type=str, default="data/raw/myntra_raw.csv")
    parser.add_argument("--delay",  type=float, default=1.5)
    args = parser.parse_args()
    scrape(pages=args.pages, output=args.output, delay=args.delay)
