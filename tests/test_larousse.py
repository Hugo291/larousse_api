"""Unit tests for the Larousse scraping client."""

from unittest.mock import Mock, patch

import pytest
import requests

from larousse_api.larousse import Larousse, LarousseError


def make_response(body, status_code=200):
    """Build a fake `requests` response wrapping `body` in an HTML page."""
    return Mock(status_code=status_code, text=f"<html><body>{body}</body></html>")


def make_larousse(body):
    """Build a Larousse instance whose page content is the given HTML body."""
    with patch("larousse_api.larousse.requests.get") as mock_get:
        mock_get.return_value = make_response(body)
        return Larousse("Fromage")


def test_get_definitions_returns_entries():
    """Definitions are extracted, tag-stripped and whitespace-normalized."""
    larousse = make_larousse(
        '<ul class="Definitions">'
        "<li>Aliment obtenu par <b>coagulation</b> du lait.</li>"
        "<li>Définition secondaire.</li>"
        "</ul>"
    )

    definitions, definition_nodes = larousse.get_definitions()

    assert definitions == [
        "Aliment obtenu par coagulation du lait.",
        "Définition secondaire.",
    ]
    assert len(definition_nodes) == 2


def test_get_synonymes_returns_entries():
    """Synonymes are read from the `Synonymes` list."""
    larousse = make_larousse(
        '<ul class="Synonymes"><li>Synonyme A</li><li>Synonyme B</li></ul>'
    )

    synonymes, synonymes_nodes = larousse.get_synonymes()

    assert synonymes == ["Synonyme A", "Synonyme B"]
    assert len(synonymes_nodes) == 2


def test_get_citations_returns_entries():
    """Citations are read from the `ListeCitations` list."""
    larousse = make_larousse(
        '<ul class="ListeCitations"><li>Citation 1</li><li>Citation 2</li></ul>'
    )

    citations, citation_nodes = larousse.get_citations()

    assert citations == ["Citation 1", "Citation 2"]
    assert len(citation_nodes) == 2


def test_get_locutions_uses_locutions_list_not_citations():
    """Locutions come from the `Locutions` list, not `ListeCitations`."""
    larousse = make_larousse(
        '<ul class="ListeCitations"><li>Citation 1</li></ul>'
        '<ul class="Locutions"><li>Locution 1</li><li>Locution 2</li></ul>'
    )

    locutions, locution_nodes = larousse.get_locutions()

    assert locutions == ["Locution 1", "Locution 2"]
    assert len(locution_nodes) == 2


def test_missing_section_returns_none():
    """A section absent from the page yields (None, None)."""
    larousse = make_larousse('<ul class="Definitions"><li>Seule section</li></ul>')

    synonymes, synonymes_nodes = larousse.get_synonymes()

    assert synonymes is None
    assert synonymes_nodes is None


def test_get_content_raises_exception_when_status_code_is_not_200():
    """A non-200 response raises LarousseError with the status code."""
    with patch("larousse_api.larousse.requests.get") as mock_get:
        mock_get.return_value = make_response("Server error", status_code=500)

        with pytest.raises(LarousseError, match="HTTP 500"):
            Larousse("Fromage")


def test_get_content_wraps_network_errors():
    """Network errors are wrapped in LarousseError."""
    with patch("larousse_api.larousse.requests.get") as mock_get:
        mock_get.side_effect = requests.ConnectionError("boom")

        with pytest.raises(LarousseError, match="failed"):
            Larousse("Fromage")


def test_request_url_uses_lowercase_word():
    """The looked-up word is lowercased in the URL and headers are sent."""
    with patch("larousse_api.larousse.requests.get") as mock_get:
        mock_get.return_value = make_response("")

        Larousse("FrOmAgE")

        assert (
            mock_get.call_args.kwargs["url"]
            == "https://www.larousse.fr/dictionnaires/francais/fromage"
        )
        assert mock_get.call_args.kwargs["timeout"] == 10
        assert "User-Agent" in mock_get.call_args.kwargs["headers"]


def test_request_url_slugifies_multi_word_entries():
    """Multi-word entries are stripped and joined with underscores."""
    with patch("larousse_api.larousse.requests.get") as mock_get:
        mock_get.return_value = make_response("")

        Larousse(" Pomme de terre ")

        assert (
            mock_get.call_args.kwargs["url"]
            == "https://www.larousse.fr/dictionnaires/francais/pomme_de_terre"
        )


def test_request_url_quotes_accented_words():
    """Accented words are percent-encoded in the URL."""
    with patch("larousse_api.larousse.requests.get") as mock_get:
        mock_get.return_value = make_response("")

        Larousse("être")

        assert (
            mock_get.call_args.kwargs["url"]
            == "https://www.larousse.fr/dictionnaires/francais/%C3%AAtre"
        )


def test_custom_timeout_is_forwarded():
    """A custom timeout is forwarded to requests.get."""
    with patch("larousse_api.larousse.requests.get") as mock_get:
        mock_get.return_value = make_response("")

        Larousse("Fromage", timeout=3)

        assert mock_get.call_args.kwargs["timeout"] == 3
