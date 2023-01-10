#!python3
import sys
from string import punctuation

tokens = []
with open(sys.argv[1]) as file:
    for line in file:
        tokens += line.translate(str.maketrans('', '', punctuation)).lower().split()

print("tokens:", len(tokens))
print("types:", len(set(tokens)))
