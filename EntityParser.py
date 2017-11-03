from spacy.en import English
import numpy as np
import re
from typing import List

class EntityParser:
    def __init__(self):
        self.parser = English()
        
        
    # Utility function to clean text before post-processing
    def cleanText(self, text: str) -> str:
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
        
    def extractEntities(self, text: str) -> np.ndarray:
        """ Accept unstructured text (e.g. a tweet)
        -> an ndarray of size n_entities by 5. Each sub-ndarray specifies
        respectively the entity text, corresponding label text, corresponding lemma,
        start index of entity and end index of entity.        
        """
        parsedEx = self.parser(text)
        listOfResults = []
        
        # extract entities
        ents = list(parsedEx.ents)
        # print("DEBUG::the entities are:")
        for entity in ents:
            #print(entity.label_, entity.start_char, entity.end_char, entity.lemma_, ' '.join(t.orth_ for t in entity))
            listOfResults.append(list((' '.join(t.orth_ for t in entity), entity.label_, entity.lemma_, 
                                       entity.start_char, entity.end_char)))
            
        return np.asarray(listOfResults)
        
    def batchExtractEntities(self, text: List[str]) -> List[np.ndarray]:
        """ Accept a list of unstructured text (e.g. a tweet)
        -> a list of ndarrays of length n_text_samples. Each entry is an ndarray of size 
        n_entities by 5. Each sub-ndarray specifies respectively the entity text, 
        corresponding label text, corresponding lemma, start index of entity and end index of entity.
        """
        
        listOfResults = []
        
        for text_sample in text:
            listOfSampleResults = []
            parsedEx = self.parser(text_sample)
        
            # extract entities
            ents = list(parsedEx.ents)
            # print("DEBUG::the entities are:")
            for entity in ents:
                #print(entity.label_, entity.start_char, entity.end_char, entity.lemma_, ' '.join(t.orth_ for t in entity))
                listOfSampleResults.append(list((' '.join(t.orth_ for t in entity), entity.label_, entity.lemma_, 
                                           entity.start_char, entity.end_char)))
                                           
            listOfResults.append(np.asarray(listOfSampleResults))
            
        return listOfResults
        
    # Tokenize the text using spaCy and convert to lemmas
    def tokenizeText(self, sample: str) -> English:

        # get the tokens using spaCy
        tokens = self.parser(sample)
    
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