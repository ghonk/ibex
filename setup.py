from setuptools import setup
# from distutils.core import setup

setup(
    name='ibex',
    version='0.1',
    description='Named entity extraction',
    author='New Knowledge',
    packages=['ibex'],
    package_data={'ibex': ['exclude_words.txt']},
    include_package_data=True,
    install_requires=[
        'spacy>=2.0.11',
        'nltk>=3.2.5',
    ],
)
