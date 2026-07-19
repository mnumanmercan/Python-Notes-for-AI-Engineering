nested = [[1, 2], [3, 4]]
kopya = nested[:]
kopya[0].append(99)

print("Original nested list:", nested)
print("Copied nested list:", kopya)

print(id(nested) == id(kopya))
print(id(nested[0]) == id(kopya[0]))