from bs4 import BeautifulSoup
from src.parsers import extract_links, extract_text, parse_html


def test_parse_and_extract():
    html = "<html><head><title>Hi</title></head><body><a href='/x'>link</a><p>Hello world</p></body></html>"
    soup = parse_html(html)
    assert soup.title.string == "Hi"
    assert extract_links(soup)[0]["text"] == "link"
    assert "Hello" in extract_text(soup)