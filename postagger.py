#!python3
import lemmaV
import os
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
    simpleTag[prp] = "PRNN"
for jj in ['JJ', 'JJR', 'JJS']:
    simpleTag[jj] = "ADJ"
for rb in ['RB', 'RBR', 'RBS', 'WRB', "RP"]:
    simpleTag[rb] = "ADV"
simpleTag["CD"] = "NUM"
simpleTag["CC"] = "CONJ"
simpleTag["UH"] = "INTR"
for dt in ['DT', 'WDT']:
    simpleTag[dt] = "DET"
for to in ['TO', 'IN']:
    simpleTag[to] = "PREP"


def tag(word: str) -> list[str]:
    """ tagging for the purpose of sending a list of possibilities to the evaluator """
    possibilities = []
    lemmas = lemmaV.lemmatizeVerb(word)
    # print(lemmas)
    for i in lemmas: # list of possible tenses if a verb
        translation = i.get("English", i['Root'])
        tags = tagPCNLP(translation)
        # tags = tagPNLTK(translation)
        # tags = tagJCNLP(translation)
        potentialTags = [simpleTag.get(tag, "UNK") for tag in tags]
        if not potentialTags:
            potentialTags = ["UNK"]
        
        # if tense == prs, it is either an actual present verb or different part of speech entirely

        # some inflection is performed, likely a verb
        if i["Tense"] != "PRS" and \
        get_highest_ranked(potentialTags) != 'VERB': # if modified but not a verb
            continue # ignore, false lemmatization
        #  print(word, "({})".format(i["Root"]), potentialTags, i["English"])
        possibilities += potentialTags
    return possibilities if possibilities else ["UNK"]

def get_highest_ranked(listOfParts:list[str]) -> str:
    """Given an list of parts of speech , return the 'strongest'"""
    if "VERB" in listOfParts:
        return "VERB"
    if "NOUN" in listOfParts:
        return "NOUN"
    if "PRNN" in listOfParts:
        return "PRNN"
    if "ADV" in listOfParts:
        return "ADV"
    if "ADJ" in listOfParts:
        return "ADJ"
    if "NUM" in listOfParts:
        return "NUM"
    if "DET" in listOfParts:
        return "DET"
    if "CONJ" in listOfParts:
        return "CONJ"
    if "PREP" in listOfParts:
        return "PREP"
    if "INTR" in listOfParts:
        return "INTR"
    else:
        print(listOfParts)
        return "UNK"


pos_tagger = nltk.parse.CoreNLPParser(url='http://localhost:9000', tagtype='pos')
def tagPCNLP(words: str):
    """ Use the Stanford CoreNLPServer"""
    return [x[1] for x in pos_tagger.tag(nltk.word_tokenize(words))]
    
def tagPNLTK(words: str):
    """ Use the NLTK POS Tagger """
    return [x[1] for x in nltk.pos_tag(words.split())]

def tagJCNLP(words: str):
    """ Create a file as input for and execute the Stanford Part of Speech Tagger.
        Return an exit code of false if something fails, as well as the output of the tagger"""
    with open('in.tag', 'w') as file:
        file.write(words)
    exitCode = os.system("cd stanford-postagger-full-2020-11-17; \
                         ./stanford-postagger.sh models/english-left3words-distsim.tagger ../in.tag > ../out.tag 2>/dev/null")
    if exitCode != 0:
        return []
    with open("out.tag") as file:
        output = file.read().split()
    return [word[word.rindex("_")+1:].strip() for word in output]

if __name__ == '__main__':
    # print(tag("Enjoying good food on the holidays, especially with family, is the best feeling to have."))
    while 1:
        print(tag(input()))