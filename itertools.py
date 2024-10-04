import itertools

# count: generate consective integers
for num in itertools.count(10, 2):
    if num > 20:
        break
    print(num)  # Output: 10, 12, 14, 16, 18, 20


# cycle: repeat element indefinitely
counter = 0
for item in itertools.cycle(["A", "B", "C"]):
    print(item)
    counter += 1
    if counter == 6:
        break

# Output: A, B, C, A, B, C

# repeat: repeat upto give value
for item in itertools.repeat("Hello", 3):
    print(item)

# Output: Hello, Hello, Hello


# combinations: return all possible combinations
items = ["A", "B", "C"]
for combo in itertools.combinations(items, 2):
    print(combo)

# Output: ('A', 'B'), ('A', 'C'), ('B', 'C')


# permuatations: give all the permutations

items = ["A", "B", "C"]
for perm in itertools.permutations(items, 2):
    print(perm)

# Output: ('A', 'B'), ('A', 'C'), ('B', 'A'), ('B', 'C'), ('C', 'A'), ('C', 'B')
