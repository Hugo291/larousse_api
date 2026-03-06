import sys
import types
from unittest.mock import Mock, patch

import pytest

# Provide lightweight fallback modules so imports succeed in restricted environments.
if "requests" not in sys.modules:
    fake_requests = types.ModuleType("requests")
    fake_requests.get = lambda **kwargs: None
    sys.modules["requests"] = fake_requests

if "bs4" not in sys.modules:
    fake_bs4 = types.ModuleType("bs4")

    class _PlaceholderBeautifulSoup:
        def __init__(self, *args, **kwargs):
            pass

    fake_bs4.BeautifulSoup = _PlaceholderBeautifulSoup
    sys.modules["bs4"] = fake_bs4

from larousse_api.larousse import Larousse


class FakeListNode:
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return f"<li>{self.text}</li>"


class FakeUl:
    def __init__(self, classes, texts):
        self._classes = classes
        self._items = [FakeListNode(text) for text in texts]

    def get(self, key):
        if key == "class":
            return self._classes
        return None

    def find_all(self, tag):
        if tag == "li":
            return self._items
        return []


class FakeSoup:
    def __init__(self, uls):
        self._uls = uls

    def find_all(self, tag):
        if tag == "ul":
            return self._uls
        return []


@patch.object(Larousse, "_Larousse__get_content")
def test_get_definitions_returns_entries(mock_get_content):
    mock_get_content.return_value = FakeSoup([FakeUl(["Definitions"], ["Définition 1", "Définition 2"])])

    larousse = Larousse("Fromage")
    definitions, definition_nodes = larousse.get_definitions()

    assert definitions == ["De\u0301finition 1", "De\u0301finition 2"]
    assert len(definition_nodes) == 2


@patch.object(Larousse, "_Larousse__get_content")
def test_get_synonymes_returns_entries(mock_get_content):
    mock_get_content.return_value = FakeSoup([FakeUl(["Synonymes"], ["Synonyme A", "Synonyme B"])])

    larousse = Larousse("Fromage")
    synonymes, synonymes_nodes = larousse.get_synonymes()

    assert synonymes == ["Synonyme A", "Synonyme B"]
    assert len(synonymes_nodes) == 2


@patch.object(Larousse, "_Larousse__get_content")
def test_get_citations_returns_entries(mock_get_content):
    mock_get_content.return_value = FakeSoup([FakeUl(["ListeCitations"], ["Citation 1", "Citation 2"])])

    larousse = Larousse("Fromage")
    citations, citation_nodes = larousse.get_citations()

    assert citations == ["Citation 1", "Citation 2"]
    assert len(citation_nodes) == 2


@patch("larousse_api.larousse.requests.get")
def test_get_content_raises_exception_when_status_code_is_not_200(mock_get):
    mock_get.return_value = Mock(status_code=500, text="Server error")

    with pytest.raises(Exception, match="Status code return an error"):
        Larousse("Fromage")


@patch("larousse_api.larousse.BeautifulSoup")
@patch("larousse_api.larousse.requests.get")
def test_request_url_uses_lowercase_word(mock_get, mock_beautiful_soup):
    mock_get.return_value = Mock(status_code=200, text="<html></html>")
    mock_beautiful_soup.return_value = Mock()

    Larousse("FrOmAgE")

    mock_get.assert_called_once_with(url="https://www.larousse.fr/dictionnaires/francais/fromage")
