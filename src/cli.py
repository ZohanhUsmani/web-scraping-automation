"""CLI entry point for scraping a list of URLs."""
import argparse
import csv
import json
from pathlib import Path

from .scraper import Scraper
from .parsers import parse_html, extract_links, extract_text


def run(urls, output, selector=None, rps=1.0):
    scraper = Scraper(rps=rps)
    rows = []
    for url in urls:
        try:
            html = scraper.fetch_text(url)
            soup = parse_html(html)
            rows.append({
                "url": url,
                "title": (soup.title.string.strip() if soup.title and soup.title.string else ""),
                "text_preview": extract_text(soup, selector)[:500],
                "link_count": len(extract_links(soup)),
            })
            print(f"OK  {url}")
        except Exception as e:
            print(f"ERR {url}: {e}")
            rows.append({"url": url, "error": str(e)})
    out = Path(output)
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.suffix == ".json":
        with open(out, "w", encoding="utf-8") as f:
            json.dump(rows, f, indent=2)
    else:
        with open(out, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["url"])
            w.writeheader()
            w.writerows(rows)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--urls", required=True, help="file with one URL per line")
    ap.add_argument("--output", default="out/results.csv")
    ap.add_argument("--selector", default=None)
    ap.add_argument("--rps", type=float, default=1.0)
    args = ap.parse_args()
    urls = [l.strip() for l in Path(args.urls).read_text().splitlines() if l.strip()]
    out = run(urls, args.output, args.selector, args.rps)
    print("Wrote", out)


if __name__ == "__main__":
    main()
