"""Larousse dictionary scraping client."""

import re
import unicodedata

import requests
from bs4 import BeautifulSoup


class LarousseError(RuntimeError):
    """Raised when Larousse content cannot be retrieved."""


class Larousse:
    """Simple client used to fetch and parse Larousse dictionary pages."""

    def __init__(self, word):
        self.word = word
        self.soup = self.__get_content()

    def get_definitions(self):
        """Return normalized definitions and original `<li>` nodes."""
        return self._extract_items("Definitions")

    def get_synonymes(self):
        """Return normalized synonymes and original `<li>` nodes."""
        return self._extract_items("Synonymes")

    def get_citations(self):
        """Return normalized citations and original `<li>` nodes."""
        return self._extract_items("ListeCitations")

    def get_locutions(self):
        """Return normalized locutions and original `<li>` nodes."""
        return self._extract_items("ListeCitations")

    def _extract_items(self, list_class):
        for ul in self.soup.find_all("ul"):
            classes = ul.get("class")
            if classes is not None and list_class in classes:
                items = ul.find_all("li")
                normalized_items = [
                    unicodedata.normalize("NFKD", re.sub("<.*?>", "", str(item)))
                    for item in items
                ]
                return normalized_items, items
        return None, None

    def __get_content(self):
        url = f"https://www.larousse.fr/dictionnaires/francais/{self.word.lower()}"
        response = requests.get(url=url, timeout=10)
        if response.status_code != 200:
            raise LarousseError("Status code return an error")
        return BeautifulSoup(response.text, "html.parser")
