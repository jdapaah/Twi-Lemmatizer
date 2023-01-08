#!python3
import sys
from characters import correction

collection = {}
filename = sys.argv[1]
with open(filename) as read, open(filename.replace("RAW", "PREPSD"), 'w') as write:
    for line in read:
        for char in line:
            if char in correction:
                write.write(correction[char])
            else:
                write.write(char)
            if char not in collection:
                collection[char] = ord(char)

collection = sorted(collection.items(), key=lambda item: item[1])
with open('collection', 'w') as f:
    for p in collection:
        print(p, file=f)