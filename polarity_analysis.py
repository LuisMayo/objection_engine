from google.cloud import translate_v2 as translate
from polyglot.detect import Detector
from polyglot.detect.base import UnknownLanguage
from polyglot.text import Text
from textblob import TextBlob
from collections import Counter

class Analizer:
    def __init__(self):
        self.official_api = True
        self.language_counter = Counter()
        try:
            self.translate_client = translate.Client()
        except Exception as e:
            print('Warning! Translator couldn\'t be initialized, fallbacking to unofficial translation engine: ' + str(e))
            self.official_api = False
    
    def get_sentiment(self, text):
        try:
            try:
                detector = Detector(text)
                language = detector.language.code
            except UnknownLanguage:
                if (len(text) <=2):
                    language = 'en'
                else:
                    language = 'google'

            self.language_counter.update({language: 1})
            print(self.language_counter)
            
            if (language == 'en'):
                return self.proccess_eng(text)

            if (language == 'google'):
                return self.process_google(text)
            
            try:
                return self.process_poly(text)
            except ZeroDivisionError:
                return 'N'
            except Exception as e:
                print(e)
                return self.process_google(text)
        except Exception as e:
            print(e)
            return self.proccess_eng(text)
        

    def process_google(self, text):
        print('Google!')
        if (self.official_api):
            result = translate_client.translate(comment.body, target_language="en")
            return self.proccess_eng(result["translatedText"])
        else: 
            return self.proccess_eng(str(TextBlob(comment.body).translate()))
        

    
    def proccess_eng(self, text):
        print('English!')
        blob = TextBlob(text)
        if (blob.sentiment.polarity > 0.05):
            return '+'
        if (blob.sentiment.polarity < -0.05):
            return '-'
        return 'N'

    def process_poly(self, text):
        print('Poly!')
        poly_text = Text(text)
        if (poly_text.polarity > 0.2):
            return '+'
        if (poly_text.polarity < -0.2):
            return '-'
        return 'N'

