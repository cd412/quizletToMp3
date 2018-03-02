from gtts import gTTS
import os
import requests
import config
# from pydub import AudioSegment


def getSet(setNumber=config.setNumber):
    '''Returns the json output of an API request for all data on a set by number.'''
    ep = '/sets/{}'.format(setNumber)
    params = {"client_id": config.quizlet_client_id,
             "whitespace": 1}
    response = requests.get(config.base_url + ep, params=params)
    data = response.json()
    return data


def getPairs(set):
    '''Accepts set and returns python dict of id, terms, and definitions.'''
    pairs = set["terms"]
    # print(pairs)
    output = {}
    for pair in pairs:
        output[pair['id']] = [pair['term'], pair['definition']]
    return output


def getTts(pairs):
    '''Converts dict of pairs into array of gTTS objects.'''
    tts = list()
    for id, pair in pairs.items():
        term = str(pair[0])
        definition = str(pair[1])
        # add try-except blocks for error 500
        # make gTTS function into its own function
        tts.append(gTTS(text=term, lang=config.termLanguage, slow=config.slow))
        tts.append(gTTS(text=definition, lang=config.defLanguage, slow=config.slow))
    return tts
            

def deleteFile(outputFile=config.outputFile):
    try:
        os.remove(outputFile)
    except FileNotFoundError:
        pass


def openFile(outputFile=config.outputFile):
    os.system(outputFile)


def writeMp3(tts, outputFile=config.outputFile):
    '''Combine clips from tts array and save to output file.'''
    deleteFile()
    with open(outputFile, 'wb') as fp:
        for clip in tts:
            clip.write_to_fp(fp)
            # addPause()


pairs = getPairs(getSet())
writeMp3(getTts(pairs))
openFile()






