from vowels import VOWEL_SML_O as o#ɔ
from vowels import VOWEL_SML_E as e#ɛ
from vowels import VOWEL_CAP_E as E#Ɛ
from vowels import VOWEL_CAP_O as O#Ɔ
from lemmaV import lemmatize

from string import punctuation
from sys import argv
"""
PRS: Present, 
FUT: Future,
PRG: Progressive,
IMF: Immediate Future,
PST: Past,
PRP: Present Perfect
"""
tenses = ['PRS', 'FUT', 'PRG', 'IMF', 'PST', 'PRP', 'PRG_N/IMF_N', 'PRS_N/FUT_N', 'PST_N', 'PRP_N']
tenses = dict(zip(tenses, [[] for _ in tenses]))
# tenses.remove('PRS')
# The present tense functions as the default in the lemmatizer
# so it removed from the statistics to avoid heavily skewing the data
for line in open(argv[1]):
    for word in line.translate(str.maketrans('', '', punctuation)).split():
        results = lemmatize(word.lower()) # list of possible tenses
        for i in results:
            tenses[i[1]].append(i)

for k, v in tenses.items():
    print(k, v)
