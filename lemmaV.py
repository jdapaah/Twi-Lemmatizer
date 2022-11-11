from vowels import VOWEL_SML_O as o#ɔ
from vowels import VOWEL_SML_E as e#ɛ
from vowels import VOWEL_CAP_E as E#Ɛ
from vowels import VOWEL_CAP_O as O#Ɔ

irregular_verbs = {"nni": 'w'+o}

# return true if the word actually exist in Twi
def existence(word):
    return True

# get the lemma of a verb in the present negative
# assumes that pronoun prefixes have been removed
def present(word: str):
    return word,

# get the lemma of a verb in the present negative
# assumes that pronoun prefixes have been removed
def presentN(word: str):
    return stdN(word)

def stdN(word: str):
    # remove the n prefix and guess the root word
    if word in irregular_verbs:
        return irregular_verbs[word]
    ret = []
    if word[:2] == 'mm': # check m or b
        for proto in ['m'+word[2:], 'b'+word[2:]]:
            if existence(proto):
                ret.append(proto)
    elif word[:2] == 'nn': # check n or d
         for proto in ['n'+word[2:], 'd'+word[2:]]:
            if existence(proto):
                ret.append(proto)
    else: # standard word
        ret = word[1:],      
    return tuple(ret)

def progressive(word: str):
    # remove the re prefix
    return word[2:],

def progressiveN(word: str):
    # remove the re+n prefix
    return stdN(word[2:])

def future(word: str):
    # remove the bɛ prefix
    return word[2:],

def futureN(word: str):
    # remove the n prefix
    return stdN(word)

def immFuture(word:str):
    # remove the re+bɛ prefix
    return word[4:],

def immFutureN(word:str):
    # remove the re+n prefix
    return progressiveN(word)

def presPerf(word: str):
    return word[1:],

def presPerfN(word: str):
    if word[-2:] in ['i'+e, 'e'+e]:
        return presentN(word[1:-2])
    else:
        return presentN(word[1:-1])


def past(word: str):
    if word[-2:] in ['i'+e, 'e'+e]:
        return word[:-2]
    else:
        return word[:-1],

def pastN(word: str):
    return stdN(word[1:])

if __name__ == '__main__':
    while 1:
        print(presentN(input()))