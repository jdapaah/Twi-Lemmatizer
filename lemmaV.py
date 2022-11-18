from vowels import VOWEL_SML_O as o#ɔ
from vowels import VOWEL_SML_E as e#ɛ
from vowels import VOWEL_CAP_E as E#Ɛ
from vowels import VOWEL_CAP_O as O#Ɔ

complement_word_ending = ['i'+e, 'e'+e]
irregular_verbs = {"nni": 'w'+o}

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


# return true if the word actually exist in Twi
def existence(word):
    if word:
        return True
    return False

def negationPrefix(word: str):
    if word[:2] in ['nn', 'mm', 'mp', 'mf']:
        return True
    if word[0] == 'n':
        return True
    return False
# return if the word can be a possible negation prefix

def lemmatize(word: str):
    # presperfN w comp
    if negationPrefix(word) and word[-1]==word[-2]: # n..xx
        return stdN(word[:-1])
    # presPerfN wo comp
    elif negationPrefix(word) and word[-2:] in complement_word_ending: # n...ie
        return stdN(word[:-2])
    # futureN, presentN
    elif negationPrefix(word): #n..
        return stdN(word)
    # def pastN(word: str):
    elif word[0] == 'a' and negationPrefix(word[1:]): # an..
        return stdN(word[1:])
    # progressive
    elif word[:2] == 're': #re..
        return word[2:],
    # progressiveN_immFutureN
    elif word[:2] == 're' and negationPrefix(word[2:]): #ren..
        return stdN(word[2:])
    # future
    elif word[:2] == 'bɛ': # be..
        return word[2:],
    # immFuture
    elif word[:4] == 'rebɛ': # rebɛ..
        return word[4:],
    # presPerf
    elif word[0] == 'a' and len(word)>3: # a..
        return word[1:],
    # def past w comp
    elif word[-2:] in complement_word_ending: #..ie
        return word[:-2],
    #past wo comp
    elif word[-1]==word[-2]: #  ..xx
        return word[:-1],
    else: # present 
        return word,

if __name__ == '__main__':
    while 1:
        print(lemmatize(input()))