#!python3
from characters import VOWEL_SMALL_O as o#ɔ
from characters import VOWEL_SMALL_E as e#ɛ

from google.cloud import translate_v2 as translate
from google.oauth2 import service_account
import enchant

complement_word_ending = ['i'+e, 'e'+e]
irregular_verbs = {"nni": 'w'+o, 'mfa': 'de'}
# Attempt optimazation of memoziation - if known attempt is not a verb, save it
credentials = service_account.Credentials.from_service_account_file("service-account.json")
translate_client = translate.Client(credentials=credentials)
englishCheck = enchant.Dict("en_GB")

def filter(words: list[dict], firstAttempt=True) -> list[dict]:
    """ Checks if the potential roots in `words` are actual words in Twi 
    (or loanwords from English). It does not check if the roots are verbs. """
    new_list = []
    for wordObj in words:
        word = wordObj["Root"]
        if firstAttempt:
            word = word.lower()
        # hard code a few words 
        if word == 'de':
            wordObj["English"] = 'put'
            new_list.append(wordObj)
        elif word == 'mo':
            wordObj["English"] = "you"
            new_list.append(wordObj)
        else:
            res = translate_client.translate(word, source_language='ak', target_language='en', format_='text')
            translationAttempt = res['translatedText']
            if translationAttempt != word or englishCheck.check(word): # if twi translation to english does not fail or its a loanword
                wordObj["English"] = translationAttempt
                new_list.append(wordObj) # is an actual lemmatized word, add to list
        
    if not new_list and firstAttempt: # if nothing with lowercase
        upped = []
        for poss in words:
            poss["Root"] = poss["Root"].capitalize() # try capitalizing
            upped.append(poss)
        return filter(upped, firstAttempt=False)
    if not new_list and not firstAttempt: # if no results from capitalizing as well
        words[-1]['Root'] = words[-1]['Root'].lower() # 
        return words[-1:] # give up and return the present without a translation [maybe its a name?]
    else:
        return new_list

def stdN(word: str):
    """ This removes the n prefix from `word` and
    returns a list of guesses of the root word. """
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


def negationPrefix(word: str):
    """ return whether or not `word` has the negation prefix """    
    if word[:2] in ['mm', 'mp', 'mf']:
        return True
    if word[0] == 'n':
        return True
    return False

def lemmatizeVerb(word: str) -> list[dict]:
    """ Lemmatize `word` without context, assuming the part of speech is a verb.
    This function operates by lemmatizing the word in all manners possible, and then
    sending a request to Google Translate to attempt to translate the proto-word 
    into English. If the attempted translations exists as a word in the English 
    language, they are returned to the client. """

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