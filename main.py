# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 17:22:41 2017

@author: azunre
"""

from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from nltk.corpus import stopwords
import string
import re
    
# Utility function to clean text before sending it to some post-processing
def cleanText(text):
    # get rid of newlines
    text = text.strip().replace("\n", " ").replace("\r", " ")
    
    # replace twitter @mentions
    mentionFinder = re.compile(r"@[a-z0-9_]{1,15}", re.IGNORECASE)
    text = mentionFinder.sub("@MENTION", text)
    
    # replace HTML symbols
    text = text.replace("&amp;", "and").replace("&gt;", ">").replace("&lt;", "<")
    
    # lowercase
    text = text.lower()

    return text

# Tokenize the text using spaCy and convert to lemmas
def tokenizeText(sample):

    # get the tokens using spaCy
    tokens = parser(sample)

    # lemmatize
    lemmas = []
    for tok in tokens:
        lemmas.append(tok.lemma_.lower().strip() if tok.lemma_ != "-PRON-" else tok.lower_)
    tokens = lemmas

    # stoplist the tokens
    tokens = [tok for tok in tokens if tok not in STOPLIST]

    # stoplist symbols
    tokens = [tok for tok in tokens if tok not in SYMBOLS]

    # remove large strings of whitespace
    while "" in tokens:
        tokens.remove("")
    while " " in tokens:
        tokens.remove(" ")
    while "\n" in tokens:
        tokens.remove("\n")
    while "\n\n" in tokens:
        tokens.remove("\n\n")

    return tokens
        
if __name__ == '__main__':
    import pandas as pd
    from random import randrange
    
    # Set up spaCy
    from spacy.en import English
    parser = English()

    # A custom stoplist
    STOPLIST = set(stopwords.words('english') + ["n't", "'s", "'m", "ca"] + list(ENGLISH_STOP_WORDS))
    # List of symbols we don't care about
    SYMBOLS = " ".join(string.punctuation).split(" ") + ["-----", "---", "...", "“", "”", "'ve"]
    
    # import selected list of tweets
    pro_gun_text = pd.read_csv('data/pro_gun_text.csv', dtype='str', header=None)
    pro_gun_text_list = pro_gun_text.ix[:,1].tolist()
    
    #print("DEBUG::the tweet list is:")
    #print(pro_gun_text_list)
    # print("DEBUG::the length of the tweet list is:")
    # print(len(pro_gun_text_list))
    
    # extract named entities of a randomly drawn sample tweet
    idx = randrange(len(pro_gun_text_list))
    example = pro_gun_text_list[idx]
    
    print("DEBUG::randomly drawn example tweet:")
    print(example)
    
    parsedEx = parser(example)
    
    # use the below code to list all tokens
    #for token in parsedEx:
    #    print(token.orth_, token.ent_type_ if token.ent_type_ != "" else "(not an entity)")

    print("-------------- the entities are: ---------------")
    # use the below code to list entities only...
    ents = list(parsedEx.ents)
    for entity in ents:
        print(entity.label, entity.label_, ' '.join(t.orth_ for t in entity))