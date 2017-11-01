#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 14:39:28 2017

@author: azunre
"""

# Set up spaCy
from spacy.en import English
parser = English()

# Test Data
multiSentence = "There is an art, it says, or rather, a knack to flying." \
                 "The knack lies in learning how to throw yourself at the ground and miss." \
                 "In the beginning the Universe was created. This has made a lot of people "\
                 "very angry and been widely regarded as a bad move."
                 
                 
# all you have to do to parse text is this:
#note: the first time you run spaCy in a file it takes a little while to load up its modules
parsedData = parser(multiSentence)

# Let's look at the tokens
# All you have to do is iterate through the parsedData
# Each token is an object with lots of different properties
# A property with an underscore at the end returns the string representation
# while a property without the underscore returns an index (int) into spaCy's vocabulary
# The probability estimate is based on counts from a 3 billion word
# corpus, smoothed using the Simple Good-Turing method.
for i, token in enumerate(parsedData):
    print("original:", token.orth, token.orth_)
    print("lowercased:", token.lower, token.lower_)
    print("lemma:", token.lemma, token.lemma_)
    print("shape:", token.shape, token.shape_)
    print("prefix:", token.prefix, token.prefix_)
    print("suffix:", token.suffix, token.suffix_)
    print("log probability:", token.prob)
    print("Brown cluster id:", token.cluster)
    print("----------------------------------------")
    if i > 1:
        break

# Let's look at the sentences
sents = []
# the "sents" property returns spans
# spans have indices into the original string
# where each index value represents a token
for span in parsedData.sents:
    # go from the start to the end of each span, returning each token in the sentence
    # combine each token using join()
    sent = ''.join(parsedData[i].string for i in range(span.start, span.end)).strip()
    sents.append(sent)

for sentence in sents:
    print(sentence)
    
# Let's look at the part of speech tags of the first sentence
for span in parsedData.sents:
    sent = [parsedData[i] for i in range(span.start, span.end)]
    break

for token in sent:
    print(token.orth_, token.pos_)
    
# Let's look at the dependencies of this example:
example = "The boy with the spotted dog quickly ran after the firetruck."
parsedEx = parser(example)
# shown as: original token, dependency tag, head word, left dependents, right dependents
for token in parsedEx:
    print(token.orth_, token.dep_, token.head.orth_, [t.orth_ for t in token.lefts], [t.orth_ for t in token.rights])
    
# Let's look at the named entities of this example:
example = "Apple's stocks dropped dramatically after the death of Steve Jobs in October."
parsedEx = parser(example)
for token in parsedEx:
    print(token.orth_, token.ent_type_ if token.ent_type_ != "" else "(not an entity)")

print("-------------- entities only ---------------")
# if you just want the entities and nothing else, you can do access the parsed examples "ents" property like this:
ents = list(parsedEx.ents)
for entity in ents:
    print(entity.label, entity.label_, ' '.join(t.orth_ for t in entity))
    
messyData = "lol that is rly funny :) This is gr8 i rate it 8/8!!!"
parsedData = parser(messyData)
for token in parsedData:
    print(token.orth_, token.pos_, token.lemma_)
    
# it does pretty well! Note that it does fail on the token "gr8", 
# taking it as a verb rather than an adjective meaning "great"
# and "lol" probably isn't a noun...it's more like an interjection
    
from numpy import dot
from numpy.linalg import norm

# you can access known words from the parser's vocabulary
nasa = parser.vocab['NASA']

# cosine similarity
cosine = lambda v1, v2: dot(v1, v2) / (norm(v1) * norm(v2))

# gather all known words, take only the lowercased versions
allWords = list({w for w in parser.vocab if w.has_vector and w.orth_.islower() and w.lower_ != "nasa"})

# sort by similarity to NASA


# THIS DOES NOT SEEM TO BE WORKING...
allWords.sort(key=lambda w: cosine(w.vector, nasa.vector))



allWords.reverse()
print("Top 10 most similar words to NASA:")
for word in allWords[:10]:   
    print(word.orth_)
    
# Let's see if it can figure out this analogy
# Man is to King as Woman is to ??
king = parser.vocab['king']
man = parser.vocab['man']
woman = parser.vocab['woman']

result = king.vector - man.vector + woman.vector

# gather all known words, take only the lowercased versions
allWords = list({w for w in parser.vocab if w.has_vector and w.orth_.islower() and w.lower_ != "king" and w.lower_ != "man" and w.lower_ != "woman"})
# sort by similarity to the result
allWords.sort(key=lambda w: cosine(w.vector, result))
allWords.reverse()
print("\n----------------------------\nTop 3 closest results for king - man + woman:")
for word in allWords[:3]:   
    print(word.orth_)
    
# it got it! Queen!

print("DEBUG::success!")