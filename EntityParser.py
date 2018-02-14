import spacy
import numpy as np
import re
from typing import List

class EntityParser:
    def __init__(self):
        self.parser = spacy.load('en')
        
        
    # Utility function to clean text before post-processing
    def cleanText(self, text: str) -> str:
        text = self.removeHashtags(text)
        text = self.removeRT(text)
        text = self.removeMentions(text)
        text = self.removeNumbers(text)
        text = self.removeDoubleSpaces(text)
        text = self.removeNewlines(text)
        text = self.removeURIs(text)
        return text

    def removeURIs(self, text: str) -> str:
        return re.sub(r'^https?:\/\/.*[\r\n]*', '', text)

    def removeHashtags(self, text: str) -> str:
        return re.sub(r'#\w*','', text)

    def removeMentions(self, text: str) -> str:
        return re.sub(r'@\w*', '', text)

    def removeNumbers(self, text: str) -> str:
        return re.sub(r'\d*', '', text)

    def removeDoubleSpaces(self, text: str) -> str:
        return re.sub(r'  ', ' ', text)
    
    def removeNewlines(self, text: str) -> str:
        return re.sub(r'\n', '', text)

    def removeRT(self, text: str) -> str:
        return re.sub(r'(RT) \@', '@', text) 

    def removeSubPhrases(self, a_list: List[str], b_list: List[str]):
        term_b_to_remove = []
        for term_a in a_list:
            for term_b in b_list:
                if term_b + ' ' in term_a or ' ' + term_b in term_a:
                    term_b_to_remove.append(term_b)
        b_list = list(set(b_list) - set(term_b_to_remove))
        return (a_list, b_list)
        
    def extractEntities(self, text: str) -> np.ndarray:
        """ Accept unstructured text (e.g. a tweet)
        -> an ndarray of size n_entities by 5. Each sub-ndarray specifies
        respectively the entity text, corresponding label text, corresponding lemma,
        start index of entity and end index of entity.        
        """
        
        # Remove hashtags and mentions before parsing
        text = self.cleanText(text)
        
        parsedEx = self.parser(text)

        # consider using lemmas instead of base words -- may do strange things to named entities
        filterFunc = lambda term: term.pos_ in ['PROPN', 'NOUN', 'VERB'] and term.dep_ in ['nsubj', 'dobj', 'pobj'] and not term.is_stop

        ents = [e.text.lower() for e in parsedEx.ents]

        otherTerms = [term.text.lower() for term in filter(filterFunc, parsedEx)]

        term_lists = self.removeSubPhrases(ents, otherTerms)
        term_lists = self.removeSubPhrases(term_lists[1], term_lists[0])

        listOfResults = list(set(term_lists[0]) | set(term_lists[1]))

        return filter(lambda x: not x == ' ', listOfResults)