import os
DEBUG = os.getenv('DEBUG', False)
PORT = os.getenv('PORT', 5000)
STOPWORD_LANGUAGES = os.getenv('STOPWORD_LANGUAGES', ['english', 'spanish'])  # 'hungarian', 'french', 'italian'

# mapping from language name to name of spacy parser
LANG_TO_PARSER = {
    'english': 'en',  # en_core_web_md
    'spanish': 'es',  # 'es_core_news_md',
}
