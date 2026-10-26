import time
import random
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
]


class RateLimiter:
    def __init__(self, rps: float = 1.0):
        self.min_interval = 1.0 / max(rps, 0.01)
        self.last = 0.0

    def wait(self):
        now = time.time()
        elapsed = now - self.last
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last = time.time()


class Scraper:
    def __init__(self, rps: float = 1.0, retries: int = 3, timeout: int = 15,
                 rotate_ua: bool = True):
        self.limiter = RateLimiter(rps)
        self.timeout = timeout
        self.rotate_ua = rotate_ua
        self.session = requests.Session()
        retry = Retry(total=retries, backoff_factor=0.5,
                      status_forcelist=[429, 500, 502, 503, 504])
        self.session.mount("http://", HTTPAdapter(max_retries=retry))
        self.session.mount("https://", HTTPAdapter(max_retries=retry))

    def _headers(self):
        h = {}
        if self.rotate_ua:
            h["User-Agent"] = random.choice(USER_AGENTS)
        return h

    def fetch(self, url: str) -> requests.Response:
        self.limiter.wait()
        resp = self.session.get(url, headers=self._headers(), timeout=self.timeout)
        resp.raise_for_status()
        return resp

    def fetch_text(self, url: str) -> str:
        return self.fetch(url).text