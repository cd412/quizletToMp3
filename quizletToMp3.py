from gtts import gTTS
import os
import requests
import config
import logging
# from pydub import AudioSegment


class Quiz:
    '''To download quizlet data and save it as an mp3 file.'''

    def __init__(self):
        '''Creates a new quiz using config file.'''
        # setup set
        self.set = self.getSet()
        self.termLanguage = self.getTermLang()
        self.defLanguage = self.getDefLang()
        
        # parse set data
        self.header = self.getHeader()
        self.pairs = self.getPairs()

        self.outputFile = config.outputFile
        log1.log(logging.DEBUG, "Quiz object created.")

    def getSet(self):
        '''Returns the json output of an API request for all data on a set by number.'''
        ep = '/sets/{}'.format(config.setNumber)
        params = {"client_id": config.quizlet_client_id,
                 "whitespace": 1}
        response = requests.get(config.base_url + ep, params=params)
        data = response.json()
        return data


    def getTermLang(self):
        '''Returns the language of the terms according to Quizlet.'''
        return self.set['lang_terms']
    

    def getDefLang(self):
        '''Returns the language of the definitions according to Quizlet.'''
        return self.set['lang_definitions']


    def getTitle(self):
        '''Returns the set title.'''
        return self.set['title']

    def getTermCount(self):
        '''Returns the number of terms in set.'''
        return self.set['term_count']

    def getHeader(self):
        '''Returns header containing title and term count.'''
        header = []
        header.append(self.getTitle())
        header.append('{} terms.'.format(self.getTermCount()))
        # date set created, date mp3 created, etc.
        return header

    def getPairs(self):
        '''Returns python dict of id, terms, and definitions.'''
        pairs = self.set['terms']
        # print(pairs)
        output = {}
        for pair in pairs:
            output[pair['id']] = [pair['term'], pair['definition']]
        return output


    def getTts(self):
        '''Converts dict of pairs into array of gTTS objects.'''
        tts = list()
        # Header
        for term in self.header:
            term = str(term)
            tts.append(gTTS(text=term, lang=self.termLanguage, slow=config.slow))
        
        # Pairs
        for id, pair in self.pairs.items():
            term = str(pair[0])
            definition = str(pair[1])
            # add try-except blocks for error 500
            # make gTTS function into its own function
            tts.append(gTTS(text=term, lang=self.termLanguage, slow=config.slow))
            tts.append(gTTS(text=definition, lang=self.defLanguage, slow=config.slow))
        return tts
            

    def deleteFile(self):
        try:
            os.remove(self.outputFile)
        except FileNotFoundError:
            pass


    def openFile(self):
        os.system(self.outputFile)


    def writeMp3(self, tts):
        '''Combine clips from tts array and save to output file.'''
        self.deleteFile()
        with open(self.outputFile, 'wb') as fp:
            for clip in tts:
                clip.write_to_fp(fp)
                # addPause()

    def run(self):
        tts = self.getTts()
        self.writeMp3(tts)
        self.openFile()


q1 = Quiz()
q1.run()







