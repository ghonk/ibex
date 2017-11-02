import string
from EntityParser import EntityParser
import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
from random import randrange

# A custom stoplist
STOPLIST = set(stopwords.words('english') + ["n't", "'s", "'m", "ca"] + list(ENGLISH_STOP_WORDS))
# List of symbols we don't care about
SYMBOLS = " ".join(string.punctuation).split(" ") + ["-----", "---", "...", "“", "”", "'ve"]

# import selected list of tweets
pro_gun_text = pd.read_csv('data/pro_gun_text.csv', dtype='str', header=None)
pro_gun_text_list = pro_gun_text.ix[:,1].tolist()

# print("DEBUG::the tweet list is:")
# print(pro_gun_text_list)
# print("DEBUG::the length of the tweet list is:")
# print(len(pro_gun_text_list))

# extract named entities of a randomly drawn sample tweet
idx = randrange(len(pro_gun_text_list))
example = pro_gun_text_list[idx]

print("DEBUG::randomly drawn example tweet:")
print(example)

NER = EntityParser()    
parsedEx = NER.parser(example)

# use the below code to list all tokens
#for token in parsedEx:
#    print(token.orth_, token.ent_type_ if token.ent_type_ != "" else "(not an entity)")

print("DEBUG::the entities are:")
# use the below code to list entities only...
ents = list(parsedEx.ents)
for entity in ents:
    print(entity.label, entity.label_, ' '.join(t.orth_ for t in entity))