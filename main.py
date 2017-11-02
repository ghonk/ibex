import pandas as pd
from random import randrange

from EntityParser import EntityParser

# import selected list of tweets
df = pd.read_csv('data/pro_gun_text.csv', dtype='str', header=None)
df_list = df.ix[:,1].tolist()

# extract named entities of a randomly drawn sample tweet
idx = randrange(len(df_list))
example = df_list[idx]

print("DEBUG::randomly drawn example tweet:")
print(example)

NER = EntityParser()    
result = NER.extractEntities(example)

print("DEBUG::the entities are:")
print(result)

print("DEBUG::the size of the result (np.ndarray) is:")
print(result.shape)