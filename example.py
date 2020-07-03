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