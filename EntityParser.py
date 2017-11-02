from spacy.en import English
import re

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