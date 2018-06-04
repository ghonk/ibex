''' Extract entities from documents '''
import os

import spacy
from nltk.corpus import stopwords

from config import STOPWORD_LANGUAGES
from preprocess import prep_text

PARSERS = {}

# languages to use nltk stopwords from
STOPWORD_LANGUAGES = ['english', 'spanish']  # 'hungarian', 'french', 'italian'
# TODO load langs from env var?

if os.path.isfile('exclude_words.txt'):
    with open('exclude_words.txt') as exclude_file:
        EXCLUDE_WORDS = set(word.strip('\n') for word in exclude_file.readlines())
else:
    # TODO move to logger
    print('warning: cant find exclude_words.txt')
    EXCLUDE_WORDS = set()

EXCLUDE_WORDS.update(*[stopwords.words(lang) for lang in STOPWORD_LANGUAGES])

KEEP_POS = ['PROPN', 'NOUN', 'VERB']
KEEP_DEP = ['nsubj', 'dobj', 'pobj']

# mapping from language name to name of spacy parser
LANG_TO_PARSER = {
    'english': 'en',
    'spanish': 'es_core_news_md',
}


def get_entities(doc: str, language: str='english'):
    ''' Takes a document and returns a list of extracted entities '''

    parser_name = LANG_TO_PARSER.get(language, '').lower()
    if not parser_name:
        raise Exception('language not currently supported')

    # if requested parser is not already in memory, try to load from spacy
    if parser_name not in PARSERS:
        PARSERS[parser_name] = spacy.load(parser_name)

    # parser = PARSERS[parser_name]
    doc = prep_text(doc)
    parsed_words = PARSERS[parser_name](doc)
    entities = set(
        word.text.lower().strip()  # TODO lowercase proper nouns?  lemmatize?
        for word in parsed_words
        if word.pos_ in KEEP_POS
        and word.dep_ in KEEP_DEP
        and not word.is_stop  # remove spacy's stopwords
    )

    # remove manually excluded words and nltk stopwords from specified languages
    entities.difference_update(EXCLUDE_WORDS)

    return list(entities)


# if __name__ == '__main__':

#     df = pd.read_csv('test.csv')
#     docs = df.content.values
#     results = [extract_entities(d, 'en') for d in docs]
#     for ents in results:
#         assert '¡' not in ents
#     print(results)
