## Larousse API

This package is a upgrade of github project [larousse_api](https://github.com/quentin-dev/larousse_api)  


### Usage
```python3
from larousse_api.larousse import Larousse

# init class larousse
l = Larousse("Fromage")

# Print the array containing all defintions of "Fromage"
print(l.get_definitions())

# Print the array containing all locution of "Fromage"
print(l.get_locutions())

# Print the array containing all synonymes of "Fromage"
print(l.get_synonymes())

# Print the array containing all citations of "Fromage"
print(l.get_citations())
```

### Why ?
Because the Larousse website doesn't supply an api to look up definitions :(

### How ?
* python3
* requests
* re
* BeautifulSoup

### Possible improvements
* Suggest words if the word is misspelled

