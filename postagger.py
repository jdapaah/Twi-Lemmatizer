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
for av in ['RB', 'RBR', 'RBS', 'WRB']:
    simpleTag[av] = "ADVERB"
simpleTag["CD"] = "NUMERAL"
simpleTag["CC"] = "CONJUNCTION"
simpleTag["UH"] = "INTERJECTION"

for dt in ['DT', 'WDT']:
    simpleTag[dt] = "DETERMINER"
for pp in ['TO', 'IN']:
    simpleTag[pp] = "PREPOSITION"


os.system("""java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer \
-preload pos \
-status_port 9000 -port 9000 -timeout 15000 & """)
pos_tagger = nltk.parse.CoreNLPParser(url='http://localhost:9000', tagtype='pos')

def tag(word: str) -> list[str]:
    """ tagging for the purpose of sending a list of possibilities to the evaluator """
    possibilities = []
    for i in lemmaV.lemmatizeVerb(word): # list of possible tenses if a verb
        success, tags = tagSFDP(i.get("English", i['Root']))
        if not success: # something went wrong with the tagging
            continue
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
                print(i)
                tags = tagSFDP(i.get("English", i['Root']))
                potentialTag = get_highest_ranked([simpleTag.get(t, t) for t in tags])
                
                # if tense == prs:
                # it is either an actual present verb or different part of speech entirely

                if i["Tense"] != "PRS" and potentialTag != 'VERB': # if modified but not a verb
                    continue # ignore, false lemmatization
                
                print(word, "({})".format(i["Root"]), potentialTag, i["English"])
                print("--")
    os.system("rm *.tag") # cleanup, remove intermediate files


def tagNLTK(words: str):
    """ Use the NLTK POS Tagger """
    return nltk.pos_tag(nltk.word_tokenize(words))

def tagSFDJ(words: str):
    """ Create a file as input for and execute the Stanford Part of Speech Tagger.
        Return an exit code of false if something fails, as well as the output of the tagger"""
    with open('in.tag', 'w') as file:
        file.write(words)
    exitCode = os.system("cd spag; \
                         ./stanford-postagger.sh models/english-left3words-distsim.tagger ../in.tag > ../out.tag 2>/dev/null")
    if exitCode != 0:
        return ""
    with open("out.tag") as file:
        output = file.read().split()
    return [word[word.rindex("_")+1:].strip() for word in output]

def tagSFDP(words: str):
    """ Use the Stanford CoreNLPServer"""
    return [x[1] for x in pos_tagger.tag(words)]

if __name__ == '__main__':
    while 1:
        print(tag(input()))
    # main()