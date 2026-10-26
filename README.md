# web-scraping-automation

Reusable web-scraping automation toolkit: fetch pages, parse with BeautifulSoup,
respect rate limits, retry on failure, rotate user-agents, export results.

## Features
- HTTP client with retries, backoff, timeout
- Rate limiter (requests/sec)
- User-agent rotation
- BeautifulSoup parsing helpers
- Export to CSV / JSON
- CLI for scraping a list of URLs

## Quick start
```bash
pip install -r requirements.txt
python -m src.cli --urls urls.txt --output out/results.csv
```
