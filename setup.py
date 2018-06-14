import os

from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install

# from distutils.core import setup


S2V_INSTALL_PATH = os.getenv('S2V_INSTALL_PATH', '/app/epfml_sent2vec')
LANGUAGES = os.getenv('STOPWORD_LANGUAGES', ['english', 'spanish'])  # 'hungarian', 'french', 'italian'
LANG_TO_PARSER = {
    'english': 'en',  # 'en_core_web_md'
    'spanish': 'es',  # 'es_core_news_md'
}
# TODO keep this synced with the languages in config/entities.py


class InstallCmd(install):
    ''' Build sent2vec FastText binary, then pip install sent2vec. '''

    def run(self):
        install.do_egg_install(self)  # instead of install.run(self)
        import nltk
        nltk.download('stopwords')
        for lang in LANGUAGES:
            os.system("python3 -m spacy download {0}".format(LANG_TO_PARSER[lang]))
        # install.run(self)


class DevelopCmd(develop):
    ''' Clone epfml's sent2vec repo, build sent2vec FastText binary, and pip install sent2vec. '''

    def run(self):
        develop.do_egg_install(self)
        import nltk
        nltk.download('stopwords')
        for lang in LANGUAGES:
            os.system("python3 -m spacy download {0}".format(LANG_TO_PARSER[lang]))
        # develop.run(self)


setup(
    name='ibex',
    version='1.0.0',
    description='Named entity extraction',
    author='New Knowledge',
    packages=['ibex'],
    package_data={'ibex': ['exclude_words.txt']},
    include_package_data=True,
    install_requires=[
        'spacy>=2.0.11',
        'nltk>=3.2.5',
        'flask>=1.0.2',
        'nose>=1.3.7',
    ],
    cmdclass={
        'install': InstallCmd,
        'develop': DevelopCmd,
    }


)