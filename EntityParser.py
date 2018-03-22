import re
import spacy
import string
import logging
import numpy as np
from typing import List

class EntityParser:
    def __init__(self):
        self.en_parser = spacy.load('en')
        self.es_parser = spacy.load('es_core_news_md')


        self.re_uri = re.compile('https?:(\/?\/?)[^\s]+')#('https?:\/\/.* ?')
        self.re_hashtags = re.compile('#\w*')
        self.re_mentions = re.compile('@\w*')
        self.re_numbers = re.compile('^\d*&')
        self.re_doublespaces = re.compile('  ')
        self.re_newlines = re.compile('\n')
        self.re_retweets = re.compile('(RT) \@')
        self.re_punctuation = re.compile('[%s]' % re.escape(string.punctuation))

        try:
            with open('excluded_words.txt', 'r') as f:
                self.excluded_words = set([word.rstrip('\n') for word in f.readlines()])
        except:
            logging.exception("Could not read 'excluded_words' file")
            self.excluded_words = set()


        
    # Utility function to clean text before post-processing
    def cleanText(self, text: str) -> str:
        text = self.removeHashtags(text)
        text = self.removeRT(text)
        text = self.removeMentions(text)
        text = self.removeDoubleSpaces(text)
        text = self.removeNewlines(text)
        text = self.removeURIs(text)
        text = self.removePunctuation(text)

        return text

    def removeURIs(self, text: str) -> str:
        return self.re_uri.sub('', text)

    def removeHashtags(self, text: str) -> str:
        return self.re_hashtags.sub('', text)

    def removeMentions(self, text: str) -> str:
        return self.re_mentions.sub('', text)

    def removeNumbers(self, text: str) -> str:
        return self.re_numbers.sub('', text)

    def removePunctuation(self, text: str) -> str:
        return self.re_punctuation.sub('', text)

    def removeDoubleSpaces(self, text: str) -> str:
        return self.re_doublespaces.sub(' ', text)
    
    def removeNewlines(self, text: str) -> str:
        return self.re_newlines.sub(' ', text)

    def removeRT(self, text: str) -> str:
        return self.re_retweets.sub('', text)

    def removeSubPhrases(self, a_list: List[str], b_list: List[str]):
        term_b_to_remove = []
        for term_a in a_list:
            for term_b in b_list:
                if term_b + ' ' in term_a or ' ' + term_b in term_a:
                    term_b_to_remove.append(term_b)
        b_list = list(set(b_list) - set(term_b_to_remove))
        return (a_list, b_list)
        
    def extractEntities(self, text: str, lang: str) -> np.ndarray:
        """ Accept unstructured text (e.g. a tweet)
        -> an ndarray of size n_entities by 5. Each sub-ndarray specifies
        respectively the entity text, corresponding label text, corresponding lemma,
        start index of entity and end index of entity.        
        """
        if lang == 'es':
            parser = self.es_parser
        else:
            parser = self.en_parser
        
        # Remove hashtags, mentions, newlines, numbers, and punctuation before parsing
        text = self.cleanText(text)

        parsedEx = parser(text)
        
        # consider using lemmas instead of base words -- may do strange things to named entities
        filterFunc = lambda term: term.pos_ in ['PROPN', 'NOUN', 'VERB'] and term.dep_ in ['nsubj', 'dobj', 'pobj'] and not term.is_stop

        numberWords = [e.text.lower() for e in filter(lambda term: term.pos_ == 'NUM', parsedEx)]        

        ents = [e.text.lower() for e in parsedEx.ents]

        ents = list(set(ents) - set(numberWords))

        otherTerms = [term.text.lower() for term in filter(filterFunc, parsedEx)]

        term_lists = self.removeSubPhrases(ents, otherTerms)
        term_lists = self.removeSubPhrases(term_lists[1], term_lists[0])

        listOfResults = list((set(term_lists[0]) | set(term_lists[1])) - self.excluded_words)
        listOfResults = [w.strip() for w in listOfResults]
        listOfResults = [self.removeNumbers(w) for w in listOfResults]
        listOfResults = [w for w in listOfResults if not w == '']

        return listOfResults

