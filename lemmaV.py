# Attempt optimazation of memoziation - if known attempt is not a verb, save it
from vowels import VOWEL_SML_O as o#ɔ
from vowels import VOWEL_SML_E as e#ɛ
from vowels import VOWEL_CAP_E as E#Ɛ
from vowels import VOWEL_CAP_O as O#Ɔ

from google.cloud import translate_v2 as translate

complement_word_ending = ['i'+e, 'e'+e]
irregular_verbs = {"nni": 'w'+o, 'mfa': 'de'}
translate_client = translate.Client()

# return true if the word actually exist in Twi
# proto word needs to be at least two characters long

def filter(words):
    new_list = []
    for wordObj in words:
        word = wordObj["Root"]
        res = translate_client.translate(word, source_language='ak', target_language='en')
        attempt = res['translatedText']
        if attempt != word: # if twi translation to english does not fail
            wordObj["English"] = attempt
            new_list.append(wordObj) # is an actual lemmatized verb, add to list
    return new_list

def stdN(word: str):
    # remove the n prefix and guess the root word
    if word in irregular_verbs:
        return [irregular_verbs[word]]
    ret = []
    if word[:2] == 'mm': # check m or b
        for proto in ['m'+word[2:], 'b'+word[2:]]:
            # if existence(proto):
            ret.append(proto)
    elif word[:2] == 'nn': # check n or d
        for proto in ['n'+word[2:], 'd'+word[2:]]:
            # if existence(proto):
            ret.append(proto)
    else:
        proto = word[1:]
        # if existence(proto): # standard word
        ret.append(proto)     
    return ret


# return if the word can be a possible negation prefix
def negationPrefix(word: str):
    if word[:2] in ['mm', 'mp', 'mf']:
        return True
    if word[0] == 'n':
        return True
    return False

"""Lemmatize the given word without context, assuming the part of speech is a verb.
   This function operates by lemmatizing the word in all manners possible, and then
   sending a request to Google Translate to attempt to translate the proto-word 
   into English. If the attempted translation exists as a word in the English 
   language, it is returned to the client."""

def lemmatizeVerb(word: str):
    results = []
    # presperfN w comp
    if negationPrefix(word) and word[-1]==word[-2]: # n..xx
        for protoRoot in stdN(word[:-1]):
            results.append({"Twi": word, "Root": protoRoot, "Tense": 'PRP_N'})
    # presPerfN wo comp
    if negationPrefix(word) and word[-2:] in complement_word_ending: # n...iɛ
        for protoRoot in stdN(word[:-2]):
            results.append({"Twi": word, "Root": protoRoot, "Tense": 'PRP_N'})
    # futureN, presentN
    if negationPrefix(word): #n..
        for protoRoot in stdN(word):
            results.append({"Twi": word, "Root": protoRoot, "Tense": 'PRS_N/FUT_N'})
    # pastN
    if word[0] == 'a' and negationPrefix(word[1:]): # an..
        for protoRoot in stdN(word[1:]):
            results.append({"Twi": word, "Root": protoRoot, "Tense":'PST_N'})
    # progressiveN_immFutureN
    if word[:2] == 're' and negationPrefix(word[2:]): #ren..
        for protoRoot in stdN(word[2:]):
            results.append({"Twi": word, "Root": protoRoot, "Tense":'PRG_N/IMF_N'})
    # progressive
    if word[:2] == 're': #re..
        results.append({"Twi": word, "Root": word[2:], "Tense": 'PRG'})
    # future
    if word[:2] == 'bɛ': # be..
        results.append({"Twi": word, "Root": word[2:], "Tense": 'FUT'})
    # immFuture
    if word[:4] == 'rebɛ': # rebɛ..
        results.append({"Twi": word, "Root": word[4:], "Tense": 'IMF'})
    # presPerf
    if word[0] == 'a': # a..
        results.append({"Twi": word, "Root": word[1:], "Tense": 'PRP'})
    # past w comp ..iɛ
    if word[-2:] in complement_word_ending :
        results.append({"Twi": word, "Root": word[:-2], "Tense": 'PST'})
    # past wo comp ..xx
    if word[-1]==word[-2]: #  
        results.append({"Twi": word, "Root": word[:-1], "Tense": 'PST'})
    results.append({"Twi": word, "Root": word, "Tense": 'PRS'})
    
    return filter(results) # filter against dictionary

if __name__ == '__main__':
    while 1:
        print(lemmatizeVerb(input()))