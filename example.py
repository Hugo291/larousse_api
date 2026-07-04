"""Example usage of the Larousse client."""

from larousse_api import Larousse

larousse = Larousse("Fromage")

# Print the list containing all definitions of "Fromage"
print(larousse.get_definitions())

# Print the list containing all locutions of "Fromage"
print(larousse.get_locutions())

# Print the list containing all synonymes of "Fromage"
print(larousse.get_synonymes())

# Print the list containing all citations of "Fromage"
print(larousse.get_citations())
