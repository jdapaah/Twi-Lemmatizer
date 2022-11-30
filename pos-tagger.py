from vowels import VOWEL_SML_O as o#ɔ
from vowels import VOWEL_SML_E as e#ɛ
from vowels import VOWEL_CAP_E as E#Ɛ
from vowels import VOWEL_CAP_O as O#Ɔ
import string

from lemmaV import lemmatize

from sys import argv
for line in open(argv[1]):
    for word in line.translate(str.maketrans('', '', string.punctuation)).split():
        results = lemmatize(word.lower())
        print(results)

