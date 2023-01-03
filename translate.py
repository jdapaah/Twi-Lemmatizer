from gc_account import PROJECT_ID

def translate(words: list[str]):
    req = createRequest(words)
    code, res = sendRequest(req)
    translations = parseResponse(res)    
    return code, translations

def createRequest(words):
    parent="projets/{}".format(PROJECT_ID)
    body = {}
    body["contents"] = words
    body["sourceLanguageCode"] = 'ak'
    body["targetLanguageCode"] = 'en'

def sendRequest(words):
    pass

def parseResponse(code, res):
    if code != 200:
        return []
    else:
        return [i['translatedText'] for i in res['translations']]