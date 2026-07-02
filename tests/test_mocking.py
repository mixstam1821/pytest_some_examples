"""
Mocking external dependencies. Interviewers often specifically ask about this
because real pipelines call external services (EUMETSAT, NASA, S3, etc.)
that you don't want to hit in a test suite.
"""
from unittest.mock import MagicMock, patch

import pytest
import requests

from src.pipeline import fetch_product_metadata


def test_fetch_product_metadata_with_unittest_mock():
    """Patch `requests.get` so no real HTTP call is made."""
    fake_response = MagicMock()
    fake_response.json.return_value = {"id": "MTG-FCI-001", "status": "ready"}
    fake_response.raise_for_status.return_value = None

    with patch("src.pipeline.requests.get", return_value=fake_response) as mock_get:
        result = fetch_product_metadata("MTG-FCI-001")

    assert result["status"] == "ready"
    mock_get.assert_called_once_with(
        "https://api.example-eo.org/products/MTG-FCI-001", timeout=10
    )


def test_fetch_product_metadata_with_monkeypatch(monkeypatch):
    """Same idea using pytest's built-in `monkeypatch` fixture instead of unittest.mock.patch."""

    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"id": "S5P-SO2-002", "status": "processing"}

    def fake_get(url, timeout):
        assert "S5P-SO2-002" in url
        return FakeResponse()

    monkeypatch.setattr(requests, "get", fake_get)
    result = fetch_product_metadata("S5P-SO2-002")
    assert result["status"] == "processing"


def test_fetch_product_metadata_propagates_http_errors():
    """Verify error handling: a 500 from the remote API should raise, not fail silently."""
    fake_response = MagicMock()
    fake_response.raise_for_status.side_effect = requests.HTTPError("500 Server Error")

    with patch("src.pipeline.requests.get", return_value=fake_response):
        with pytest.raises(requests.HTTPError):
            fetch_product_metadata("BROKEN-ID")
