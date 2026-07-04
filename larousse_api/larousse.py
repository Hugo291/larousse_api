"""Larousse dictionary scraping client."""

from __future__ import annotations

import re
import unicodedata
from typing import List, Optional, Tuple
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.larousse.fr/dictionnaires/francais/"
DEFAULT_TIMEOUT = 10
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)


class LarousseError(RuntimeError):
    """Raised when Larousse content cannot be retrieved."""


class Larousse:
    """Simple client used to fetch and parse Larousse dictionary pages."""

    def __init__(self, word: str, timeout: float = DEFAULT_TIMEOUT):
        self.word = word
        self.timeout = timeout
        self.soup = self.__get_content()

    def get_definitions(self) -> Tuple[Optional[List[str]], Optional[list]]:
        """Return normalized definitions and original `<li>` nodes."""
        return self._extract_items("Definitions")

    def get_synonymes(self) -> Tuple[Optional[List[str]], Optional[list]]:
        """Return normalized synonymes and original `<li>` nodes."""
        return self._extract_items("Synonymes")

    def get_citations(self) -> Tuple[Optional[List[str]], Optional[list]]:
        """Return normalized citations and original `<li>` nodes."""
        return self._extract_items("ListeCitations")

    def get_locutions(self) -> Tuple[Optional[List[str]], Optional[list]]:
        """Return normalized locutions and original `<li>` nodes."""
        return self._extract_items("Locutions")

    def _extract_items(
        self, list_class: str
    ) -> Tuple[Optional[List[str]], Optional[list]]:
        for unordered_list in self.soup.find_all("ul"):
            classes = unordered_list.get("class")
            if classes is not None and list_class in classes:
                items = unordered_list.find_all("li")
                normalized_items = [
                    self._normalize_text(item) for item in items
                ]
                return normalized_items, items
        return None, None

    @staticmethod
    def _normalize_text(item) -> str:
        text = unicodedata.normalize("NFKC", item.get_text(" "))
        return re.sub(r"\s+", " ", text).strip()

    def __get_content(self) -> BeautifulSoup:
        slug = quote(self.word.strip().lower().replace(" ", "_"))
        url = f"{BASE_URL}{slug}"
        try:
            response = requests.get(
                url=url,
                headers={"User-Agent": USER_AGENT},
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            raise LarousseError(f"Request to {url} failed: {exc}") from exc
        if response.status_code != 200:
            raise LarousseError(
                f"Larousse returned HTTP {response.status_code} "
                f"for word {self.word!r} ({url})"
            )
        return BeautifulSoup(response.text, "html.parser")
