## Larousse API

This package is an upgrade of the GitHub project [larousse_api](https://github.com/quentin-dev/larousse_api).

It scrapes [larousse.fr](https://www.larousse.fr/dictionnaires/francais) to look up
definitions, synonyms, citations and locutions of French words.

### Installation

```bash
pip install .
```

### Usage

```python
from larousse_api import Larousse, LarousseError

try:
    larousse = Larousse("Fromage")
except LarousseError as error:
    # Raised when the word cannot be found or the request fails
    print(error)
else:
    # Each getter returns a tuple (normalized_texts, raw_li_nodes).
    # Both values are None when the section is missing for the word.
    definitions, _ = larousse.get_definitions()
    locutions, _ = larousse.get_locutions()
    synonymes, _ = larousse.get_synonymes()
    citations, _ = larousse.get_citations()

    print(definitions)
    print(locutions)
    print(synonymes)
    print(citations)
```

Multi-word entries and accented words are handled automatically
(`Larousse("pomme de terre")`, `Larousse("être")`), and a custom request
timeout can be passed with `Larousse("Fromage", timeout=5)`.

### Why?

Because the Larousse website doesn't supply an API to look up definitions :(

### How?

* python3 (>= 3.10)
* [requests](https://pypi.org/project/requests/)
* [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)

### Development

```bash
pip install -r requirements.txt
python -m pytest -q
```

### Possible improvements

* Suggest words if the word is misspelled
