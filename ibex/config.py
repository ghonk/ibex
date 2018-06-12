import os
DEBUG = os.getenv('DEBUG', False)
PORT = os.getenv('PORT', 5000)
STOPWORD_LANGUAGES = os.getenv('STOPWORD_LANGUAGES', ['english', 'spanish'])  # 'hungarian', 'french', 'italian'
