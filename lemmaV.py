from vowels import VOWEL_SML_O as o#ɔ
from vowels import VOWEL_SML_E as e#ɛ
from vowels import VOWEL_CAP_E as E#Ɛ
from vowels import VOWEL_CAP_O as O#Ɔ

complement_word_ending = ['i'+e, 'e'+e]
irregular_verbs = {"nni": 'w'+o, 'mfa': 'de'}

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
    else:
        proto = word[1:]
        if existence(proto): # standard word
            ret.append(proto)     
    return tuple(ret)


# return true if the word actually exist in Twi
# proto word needs to be at least two characters long
def existence(word):
    if word and len(word)>=2:
        return True
    return False

def negationPrefix(word: str):
    if word[:2] in ['mm', 'mp', 'mf']:
        return True
    if word[0] == 'n':
        return True
    return False
# return if the word can be a possible negation prefix

def lemmatize(word: str):
    results = []
    # presperfN w comp
    if negationPrefix(word) and word[-1]==word[-2]: # n..xx
        results.append(stdN(word[:-1])+('PRP_N',))
    # presPerfN wo comp
    elif negationPrefix(word) and word[-2:] in complement_word_ending: # n...ie
        results.append(stdN(word[:-2])+('PRP_N',))
    # futureN, presentN
    elif negationPrefix(word): #n..
        results.append(stdN(word)+('PRS_N/FUT_N',))
    # def pastN(word: str):
    elif word[0] == 'a' and negationPrefix(word[1:]): # an..
        results.append(stdN(word[1:])+('PST_N',))
    # progressiveN_immFutureN
    elif word[:2] == 're' and negationPrefix(word[2:]): #ren..
        results.append(stdN(word[2:])+('PRG_N/IMF_N',))
    # progressive
    elif word[:2] == 're': #re..
        results.append((word[2:],'PRG'))
    # future
    elif word[:2] == 'bɛ': # be..
        results.append((word[2:],'FUT'))
    # immFuture
    elif word[:4] == 'rebɛ': # rebɛ..
        results.append((word[4:],'IMF'))
    # presPerf
    elif word[0] == 'a' and len(word)>3: # a..
        results.append((word[1:],'PRP'))
    # def past w comp
    elif word[-2:] in complement_word_ending: #..ie
        results.append((word[:-2],'PST'))
    #past wo comp
    elif word[-1]==word[-2]: #  ..xx
        results.append((word[:-1],'PST'))
    # else: # present 
    #     results.append((word,'PRS'))
    return results # filter against dictionary

if __name__ == '__main__':
    while 1:
        print(lemmatize(input()))