#!python3
import lemmaV

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
for rb in ['RB', 'RBR', 'RBS', 'WRB']:
    simpleTag[rb] = "ADVERB"
simpleTag["CD"] = "NUMERAL"
simpleTag["CC"] = "CONJUNCTION"
simpleTag["UH"] = "INTERJECTION"
for dt in ['DT', 'WDT']:
    simpleTag[dt] = "DETERMINER"
for to in ['TO', 'IN']:
    simpleTag[to] = "PREPOSITION"


def tag(word: str) -> list[str]:
    """ tagging for the purpose of sending a list of possibilities to the evaluator """
    possibilities = []
    for i in lemmaV.lemmatizeVerb(word): # list of possible tenses if a verb
        tags = tagSFDP(i.get("English", i['Root']))
        # tags = tagNLTK(i.get("English", i['Root']))
        # tags = tagSFDJ(i.get("English", i['Root']))
        potentialTags = [simpleTag.get(tag, tag) for tag in tags]
        
        # if tense == prs:
            # it is either an actual present verb or different part of speech entirely

        if i["Tense"] != "PRS": # some inflection is performed, likely a verb
            # if get_highest_ranked(potentialTags) != 'VERB': # if modified but not a verb
            if 'VERB' not in potentialTags: # if modified but not a verb
                continue # ignore, false lemmatization
        
        possibilities += potentialTags
    return possibilities

def get_highest_ranked(listOfParts:list[str]) -> str:
    """Given an list of parts of speech , return the 'strongest'"""
    if "VERB" in listOfParts:
        return "VERB"
    if "NOUN" in listOfParts:
        return "NOUN"
    if "PRONOUN" in listOfParts:
        return "PRONOUN"
    if "ADVERB" in listOfParts:
        return "ADVERB"
    if "ADJECTIVE" in listOfParts:
        return "ADJECTIVE"
    if "NUMERAL" in listOfParts:
        return "NUMERAL"
    if "DETERMINER" in listOfParts:
        return "DETERMINER"
    if "CONJUNCTION" in listOfParts:
        return "CONJUNCTION"
    if "PREPOSITION" in listOfParts:
        return "PREPOSITION"
    else:
        return "INTERJECTION"
    

def main():
    for line in open(argv[1]):
        for word in line.translate(str.maketrans('', '', '!,.?')).split():
            print("-----")
            for i in lemmaV.lemmatizeVerb(word): # list of possible tenses if a verb
                tags = tagSFDP(i.get("English", i['Root']))
                potentialTag = get_highest_ranked([simpleTag.get(t, t) for t in tags])
                
                # if tense == prs:
                # it is either an actual present verb or different part of speech entirely

                if i["Tense"] != "PRS" and potentialTag != 'VERB': # if modified but not a verb
                    continue # ignore, false lemmatization
                
                print(word, "({})".format(i["Root"]), potentialTag, i["English"])
                print("--")
    os.system("rm *.tag") # cleanup, remove intermediate files


pos_tagger = nltk.parse.CoreNLPParser(url='http://localhost:9000', tagtype='pos')
def tagSFDP(words: str):
    """ Use the Stanford CoreNLPServer"""
    return [x[1] for x in pos_tagger.tag(words.split())]
    
def tagNLTK(words: str):
    """ Use the NLTK POS Tagger """
    return [x[1] for x in nltk.pos_tag(words.split())]

def tagSFDJ(words: str):
    """ Create a file as input for and execute the Stanford Part of Speech Tagger.
        Return an exit code of false if something fails, as well as the output of the tagger"""
    with open('in.tag', 'w') as file:
        file.write(words)
    exitCode = os.system("cd stanford-postagger-full-2020-11-17; \
                         ./stanford-postagger.sh models/english-left3words-distsim.tagger ../in.tag > ../out.tag 2>/dev/null")
    if exitCode != 0:
        return "UNKNOWN"
    with open("out.tag") as file:
        output = file.read().split()
    return [word[word.rindex("_")+1:].strip() for word in output]

if __name__ == '__main__':
    print(tag("Enjoying good food on the holidays, especially with family, is the best feeling to have."))
    # while 1:
        # print(tag("input()"))
    # main()