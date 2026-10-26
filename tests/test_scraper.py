import pytest
from unittest.mock import patch, MagicMock
from src.scraper import Scraper


def test_fetch_uses_session():
    s = Scraper(rps=100, retries=1)
    mock_resp = MagicMock()
    mock_resp.text = "<html>ok</html>"
    mock_resp.raise_for_status = lambda: None
    with patch.object(s.session, "get", return_value=mock_resp):
        r = s.fetch_text("https://example.com")
    assert r == "<html>ok</html>"