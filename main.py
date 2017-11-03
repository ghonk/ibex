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


# next, demo the batch processing function
idx = randrange(len(df_list)-5)
many_examples = df_list[idx:idx+5]

print("DEBUG::randomly drawn example tweet batch:")
print(many_examples)

result = NER.batchExtractEntities(many_examples)

print("DEBUG::the entities are:")
print(result)

print("DEBUG::the length of the result (list of np.ndarrays) is:")
print(len(result))