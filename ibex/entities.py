''' Extract named entities from documents '''
import os

import spacy
from nltk.corpus import stopwords

from .config import STOPWORD_LANGUAGES
from .preprocess import prep_text

PARSERS = {}

if os.path.isfile('ibex/exclude_words.txt'):
    with open('ibex/exclude_words.txt') as exclude_file:
        EXCLUDE_WORDS = set(word.strip('\n') for word in exclude_file.readlines())
else:
    # TODO move to logger
    print('warning: cant find exclude_words.txt')
    EXCLUDE_WORDS = set()

EXCLUDE_WORDS.update(*[stopwords.words(lang) for lang in STOPWORD_LANGUAGES])


# mapping from language name to name of spacy parser
LANG_TO_PARSER = {
    'english': 'en',
    'spanish': 'es_core_news_sm',
}


def is_stop_word(entity):
    if len(entity) == 1:
        ent = entity[0]
        return ent.is_stop or ent.text in EXCLUDE_WORDS
    return False


def get_entities(doc: str, language: str='english'):
    ''' Takes a document and returns a list of extracted entities '''

    parser_name = LANG_TO_PARSER.get(language, '').lower()
    if not parser_name:
        raise Exception('language not currently supported')

    # if requested parser is not already in memory, try to load from spacy
    if parser_name not in PARSERS:
        PARSERS[parser_name] = spacy.load(parser_name)

    doc = prep_text(doc)
    parsed_doc = PARSERS[parser_name](doc)
    entities = [ent.text for ent in parsed_doc.ents if not is_stop_word(ent)]

    return entities


# KEEP_POS = ['PROPN', 'NOUN', 'VERB']
# KEEP_DEP = ['nsubj', 'dobj', 'pobj']

    # print('spacy entities:', list(parsed_doc.ents))
    # entities = set(
    #     word.text.lower().strip()  # TODO lowercase proper nouns?  lemmatize?
    #     for word in parsed_doc
    #     if word.pos_ in KEEP_POS
    #     and word.dep_ in KEEP_DEP
    #     and not word.is_stop  # remove spacy's stopwords
    # )

    # remove manually excluded words and nltk stopwords from specified languages
    # entities.difference_update(EXCLUDE_WORDS)


# def removeSubPhrases(self, a_list: List[str], b_list: List[str]):
#         term_b_to_remove = []
#         for term_a in a_list:
#             for term_b in b_list:
#                 if term_b + ' ' in term_a or ' ' + term_b in term_a:
#                     term_b_to_remove.append(term_b)
#         b_list = list(set(b_list) - set(term_b_to_remove))
#         return (a_list, b_list)

#     def extractEntities(self, text: str, lang: str) -> np.ndarray:
#         """ Accept unstructured text (e.g. a tweet)
#         -> an ndarray of size n_entities by 5. Each sub-ndarray specifies
#         respectively the entity text, corresponding label text, corresponding lemma,
#         start index of entity and end index of entity.
#         """
#         if lang == 'es':
#             parser = self.es_parser
#         else:
#             parser = self.en_parser

#         # Remove hashtags, mentions, newlines, numbers, and punctuation before parsing
#         text = self.cleanText(text)

#         parsedEx = parser(text)

#         # consider using lemmas instead of base words -- may do strange things to named entities
#         filterFunc = lambda term: term.pos_ in ['PROPN', 'NOUN', 'VERB'] and term.dep_ in ['nsubj', 'dobj', 'pobj'] and not term.is_stop

#         numberWords = [e.text.lower() for e in filter(lambda term: term.pos_ == 'NUM', parsedEx)]

#         ents = [e.text.lower() for e in parsedEx.ents]

#         ents = list(set(ents) - set(numberWords))

#         otherTerms = [term.text.lower() for term in filter(filterFunc, parsedEx)]

#         term_lists = self.removeSubPhrases(ents, otherTerms)
#         term_lists = self.removeSubPhrases(term_lists[1], term_lists[0])

#         listOfResults = list((set(term_lists[0]) | set(term_lists[1])) - self.excluded_words)
#         listOfResults = [w.strip() for w in listOfResults]
#         listOfResults = [self.removeNumbers(w) for w in listOfResults]
#         listOfResults = [w for w in listOfResults if not w == '']

#         return listOfResults
