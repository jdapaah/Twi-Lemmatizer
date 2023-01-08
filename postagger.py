#!python3
from lemmaV import lemmatizeVerb

from string import punctuation
from sys import argv
import os
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

simpleTag = {} # provide a mapping from the detailed parts of speech in English to smaller, simpler set
for vb in ['VB', 'VBP', 'VBZ', 'VBD', 'VBN', 'VBG', 'MD']:
    simpleTag[vb] = "VERB"
for nn in ['NN', 'NNS', 'NNP',  'NNPS']:
    simpleTag[nn] = "NOUN"
for prp in ['PRP', 'PRP$', 'WP', 'WP$']:
    simpleTag[prp] = "PRONOUN"
for jj in ['JJ', 'JJR', 'JJS']:
    simpleTag[jj] = "ADJECTIVE"
for av in ['RB', 'RBR', 'RBS', 'WRB']:
    simpleTag[av] = "ADVERB"
simpleTag["CD"] = "NUMERAL"
simpleTag["CC"] = "CONJUNCTION"
simpleTag["UH"] = "INTERJECTION"

for dt in ['DT', 'WDT']:
    simpleTag[dt] = "DETERMINER"
for pp in ['TO', 'IN']:
    simpleTag[pp] = "PREPOSITION"

def tag(word: str) -> list[str]:
    """ tagging for the purpose of sending a list of possibilities to the evaluator """
    possibilities = []
    for i in lemmatizeVerb(word): # list of possible tenses if a verb
        success, tag = tagSFDJ(i.get("English"))
        if not success: # something went wrong with the tagging
            continue
        potentialTag = simpleTag.get(tag, tag)
        
        # if tense == prs:
        # it is either an actual present verb or different part of speech entirely

        if i["Tense"] != "PRS": # some inflection is performed, likely a verb
            if i["Tense"] in ['PRS_N/FUT_N', 'PRP_N']: # n..
                pass
                # potentialTag += "_POSSIBLE-PLURAL-NOUN" # could be a plural noun?
            elif potentialTag != 'VERB': # if modified but not a verb
                continue # ignore, false lemmatization
        
        possibilities.append(potentialTag)

def get_highest_ranked(listOfParts:list[str]) -> str:
    """Given an list of parts of speech , return the 'strongest'"""
    return listOfParts[-1]

def main():
    for line in open(argv[1]):
        for word in line.translate(str.maketrans('', '', punctuation)).split():
            print("-----")
            for i in lemmatizeVerb(word): # list of possible tenses if a verb
                print(i)
                success, tag = tagWord(i.get("English"))
                if not success: # something went wrong with the tagging
                    continue
                potentialTag = simpleTag.get(tag, tuple(tag) if type(tag)==list else tag)
                
                # if tense == prs:
                # it is either an actual present verb or different part of speech entirely

                if i["Tense"] != "PRS": # some inflection is performed, likely a verb
                    if i["Tense"] in ['PRS_N/FUT_N', 'PRP_N']: # n..
                        pass
                        # potentialTag += "_POSSIBLE-PLURAL-NOUN" # could be a plural noun?
                    elif potentialTag != 'VERB': # if modified but not a verb
                        continue # ignore, false lemmatization
                
                print(word, "({})".format(i["Root"]), potentialTag, i["English"])
                print("--")
    os.system("rm *.tag") # cleanup, remove intermediate files


def tagNLTK(word):
    """ Use the NLTK POS Tagger """
    return nltk.pos_tag([word])[0]

def tagSFDJ(word):
    """ Create a file as input for and execute the Stanford Part of Speech Tagger.
        Return an exit code of false if something fails, as well as the output of the tagger"""
    if word == "": # word was never translated
        return True, "UNKNOWN"
    with open('in.tag', 'w') as file:
        file.write(word)
    exitCode = os.system("cd stanford-postagger-full-2020-11-17; \
                         ./stanford-postagger.sh models/english-left3words-distsim.tagger ../in.tag > ../out.tag 2>/dev/null")
    if exitCode != 0:
        return False, ""
    with open("out.tag") as file:
        output = file.read().split()
    return True, get_highest_ranked([word[word.rindex("_")+1:].strip() for word in output])

def tagWord(word):
    if word == "": # word was never translated
        return True, "UNKNOWN"
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