import json

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
counts = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}}

with open("words.txt") as file:
    for line in file:
        temp = 0
        for char in line.strip():
            if char in counts[temp]:
                counts[temp][char] += 1
            else:
                counts[temp][char] = 1
            temp += 1

# Fill in missing letters
for char in ALPHABET:
    for i in range(5):
        if char not in counts[i]:
            counts[i][char] = 0

with open("wordcount_output.json", 'w') as file:
    json.dump(counts, file)