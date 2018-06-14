''' Extract named entities from documents '''
import os

import spacy
from nltk.corpus import stopwords
from typing import List
from .config import STOPWORD_LANGUAGES, LANG_TO_PARSER
from .preprocess import prep_text


PARSERS = {}

current_path = os.path.dirname(os.path.abspath(__file__))
exclude_path = os.path.join(current_path, 'exclude_words.txt')
if os.path.isfile(exclude_path):
    with open(exclude_path) as exclude_file:
        EXCLUDE_WORDS = set(word.strip('\n') for word in exclude_file.readlines())
else:
    # TODO move to logger
    print('warning: cant find exclude_words.txt')
    EXCLUDE_WORDS = set()

EXCLUDE_WORDS.update(*[stopwords.words(lang) for lang in STOPWORD_LANGUAGES])


def filter_entity(entity):
    ''' filter entities identified by spacey. For single-word entities, remove
    those in the exclude list or not proper nouns. for multi-word entities, make
    sure all words are not stop words with some exceptions.
    '''

    if len(entity) == 1:
        # for single word entities, remove if stop word or number
        ent = entity[0]
        return (ent.is_stop or ent.text.lower() in EXCLUDE_WORDS
                or ent.pos_ != 'PROPN'
                # or ent.pos_ == 'NUM'
                # or ent.pos_ == 'PUNCT')
                )
        # TODO allow single entities that are not tagged as a proper noun?

    # for multi-word entities, remove if there are any stop words with exceptions for some POS
    remove = [(word.is_stop or (word.text.lower() in EXCLUDE_WORDS))
              # allow determiners that are not wh-determiners or interrogatives
              and not (word.pos_ == 'DET' and word.tag_ != 'WDT' and word.tag_ != 'DET__PronType=Int')
              and word.pos_ != 'ADP'  # and adpositions
              for word in entity]

    return any(remove)


def get_entities(docs: List(str), language: str='english'):
    ''' Takes a document and returns a list of extracted entities '''

    # if language given is not the name of a spacy parser, try to convert it to one
    parser_name = language if language in LANG_TO_PARSER.values() else LANG_TO_PARSER.get(language.lower())
    if not parser_name:
        raise Exception('language not supported')

    # if requested parser is not already in memory, try to load from spacy
    if parser_name not in PARSERS:
        PARSERS[parser_name] = spacy.load(parser_name)

    def get_ents(doc):
        ''' prep, parse, then extract entities from doc text '''
        doc = prep_text(doc)  # preprocess string
        doc = PARSERS[parser_name](doc)  # parse prepped doc
        ents = set(ent.text for ent in doc.ents if not filter_entity(ent))  # extract entities
        return list(ents)

    return [get_ents(doc) for doc in docs]


def produce(docs: List(str), language: str='english'):
    return get_entities(docs, language)
