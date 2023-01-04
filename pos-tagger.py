#!python3
from vowels import VOWEL_SML_O as o#ɔ
from vowels import VOWEL_SML_E as e#ɛ
from vowels import VOWEL_CAP_E as E#Ɛ
from vowels import VOWEL_CAP_O as O#Ɔ
from lemmaV import lemmatizeVerb

from string import punctuation
from sys import argv
import os
import time
import stanza
import nltk

"""
PRS: Present, 
FUT: Future,
PRG: Progressive,
IMF: Immediate Future,
PST: Past,
PRP: Present Perfect
"""
tenses = {key: [] for key in ['PRS', 'FUT', 'PRG', 'IMF', 'PST', 'PRP',
                            'PRS_N/FUT_N', 'PRG_N/IMF_N', 'PST_N', 'PRP_N']}

simpleTag = {} # provide a mapping from the detailed parts of speech in English to smaller, simpler set
for v in ['VB', 'VBP', 'VBZ', 'VBD', 'VBN', 'VBG']:
    simpleTag[v] = "VERB"
for n in ['NN', 'NNS', 'NNP',  'NNPS', 'PRP']:
    simpleTag[n] = "NOUN"
for j in ['JJ', 'JJR', 'JJS']:
    simpleTag[j] = "ADJ"
for a in ['RB', 'RBR', 'RBS']:
    simpleTag[a] = "ADVERB"
for p in ['TO', 'IN']:
    simpleTag[p] = "PREPOS"

# The present tense functions as the default in the lemmatizer
# so it removed from the statistics to avoid heavily skewing the data
def main():
    for line in open(argv[1]):
        for word in line.translate(str.maketrans('', '', punctuation)).split():
            print("-----")
            for i in lemmatizeVerb(word.lower()): # list of possible tenses if a verb
                success, tag = tagWord(i["English"])
                if not success: # something went wrong with the tagging
                    continue
                potentialTag = simpleTag.get(tag, tag)
                
                # if tense == prs:
                # it is either an actual present verb or different part of speech entirely

                if i["Tense"] != "PRS": # some inflection is performed, likely a verb
                    if i["Tense"] in ['PRS_N/FUT_N', 'PRP_N']: # n..
                        potentialTag += "_POSSIBLE-PLURAL-NOUN" # could be a plural noun?
                    elif potentialTag != 'VERB': # if modified but not a verb
                        continue # ignore, false lemmatization
                
                print(word, i["Root"], potentialTag, i["English"])
                print("--")
    os.system("rm *.tag") # cleanup, remove intermediate files

""" Create a file as input for and execute the Stanford Part of Speech Tagger.
    Return an exit code of false if something fails, as well as the output of the tagger"""

def tagWord(word):
    return nltk.pos_tag([word])[0]

def tagWordO(word):
    with open('in.tag', 'w') as file:
        file.write(word)
    exitCode = os.system("cd stanford-postagger-full-2020-11-17; \
                         ./stanford-postagger.sh models/english-left3words-distsim.tagger ../in.tag > ../out.tag 2>/dev/null")
    if exitCode != 0:
        return False, ""
    with open("out.tag") as file:
        output = file.read()
    return True, output[output.rindex("_")+1:].strip()

if __name__ == '__main__':
    main()