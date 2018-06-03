import re
import spacy
import string
import logging
import numpy as np
from typing import List
from nltk.corpus import stopwords
import pandas as pd

LANGUAGES = ['english', 'spanish']  # 'hungarian', 'french', 'italian'


class EntityParser:
    def __init__(self):
        self.en_parser = spacy.load('en')
        self.es_parser = spacy.load('es_core_news_md')
        # self.xx_parser = spacy.load('xx')  # cross language parser

        self.re_uri = re.compile('https?:(\/?\/?)[^\s]+')  # ('https?:\/\/.* ?')
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

        for lang in LANGUAGES:
            # remove stop words for all relevant languages
            self.excluded_words.update(stopwords.words(lang))

    # Utility function to clean text before post-processing
    def clean_text(self, text: str) -> str:
        text = self.remove_hashtags(text)
        text = self.remove_retweets(text)
        text = self.remove_mentions(text)
        text = self.remove_doubleSpaces(text)
        text = self.remove_newlines(text)
        text = self.remove_URIs(text)
        text = self.remove_punctuation(text)

        return text

    def remove_URIs(self, text: str) -> str:
        return self.re_uri.sub('', text)

    def remove_hashtags(self, text: str) -> str:
        return self.re_hashtags.sub('', text)

    def remove_mentions(self, text: str) -> str:
        return self.re_mentions.sub('', text)

    def remove_numbers(self, text: str) -> str:
        return self.re_numbers.sub('', text)

    def remove_punctuation(self, text: str) -> str:
        return self.re_punctuation.sub('', text)

    def remove_doubleSpaces(self, text: str) -> str:
        return self.re_doublespaces.sub(' ', text)

    def remove_newlines(self, text: str) -> str:
        return self.re_newlines.sub(' ', text)

    def remove_retweets(self, text: str) -> str:
        return self.re_retweets.sub('', text)

    def remove_sub_phrases(self, a_list: List[str], b_list: List[str]):
        term_b_to_remove = []
        for term_a in a_list:
            for term_b in b_list:
                if term_b + ' ' in term_a or ' ' + term_b in term_a:
                    term_b_to_remove.append(term_b)
        b_list = list(set(b_list) - set(term_b_to_remove))
        return (a_list, b_list)

    def extract_entities(self, text: str, lang: str) -> np.ndarray:
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
        text = self.clean_text(text)

        parsedEx = parser(text)

        # consider using lemmas instead of base words -- may do strange things to named entities
        def filterFunc(term): return term.pos_ in ['PROPN', 'NOUN', 'VERB'] and term.dep_ in [
            'nsubj', 'dobj', 'pobj'] and not term.is_stop

        number_words = [e.text.lower() for e in filter(lambda term: term.pos_ == 'NUM', parsedEx)]

        ents = [e.text.lower() for e in parsedEx.ents]

        ents = list(set(ents) - set(number_words))

        other_terms = [term.text.lower() for term in filter(filterFunc, parsedEx)]

        term_lists = self.remove_sub_phrases(ents, other_terms)
        term_lists = self.remove_sub_phrases(term_lists[1], term_lists[0])

        results = list((set(term_lists[0]) | set(term_lists[1])) - self.excluded_words)
        results = [w.strip() for w in results]
        results = [self.remove_numbers(w) for w in results]
        results = [w for w in results if w != '']

        return results


if __name__ == '__main__':

    df = pd.read_csv('test.csv')
    docs = df.content.values

    ep = EntityParser()
    ents = [ep.extract_entities(d, 'spanish') for d in docs]
    print(ents)
