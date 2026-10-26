"""Parsing helpers built on BeautifulSoup."""
from bs4 import BeautifulSoup


def parse_html(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "lxml")


def extract_links(soup: BeautifulSoup, base_url: str = "") -> list[dict]:
    out = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        text = a.get_text(strip=True)
        out.append({"text": text, "href": href})
    return out


def extract_text(soup: BeautifulSoup, selector: str = None) -> str:
    if selector:
        el = soup.select_one(selector)
        return el.get_text(" ", strip=True) if el else ""
    return soup.get_text(" ", strip=True)[:5000]