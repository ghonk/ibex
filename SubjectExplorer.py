# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 09:13:37 2017

@author: azunre
"""

# sumy imports
from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

# other imports
import numpy as np
import pandas as pd
import scipy.sparse as ssp
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List

# Hyper settings...
LANGUAGE = "english"
SENTENCES_COUNT = 20
DEBUG = False
MAX_N_ROWS = 10000

class SubjectExplorer:
    def __init__(self):
        self.stemmer = Stemmer(LANGUAGE)
        self.summarizer = Summarizer(self.stemmer)
        self.summarizer.stop_words = get_stop_words(LANGUAGE)

    def ExtractivelySummarizeCorpus(self,corpus_path:str,HTML:bool = True)->List[str]:

        if(HTML):
            self.parser = HtmlParser.from_url(corpus_path, Tokenizer(LANGUAGE))
        else:
            # or for plain text files
            self.parser = PlaintextParser.from_file(corpus_path, Tokenizer(LANGUAGE))
        
        sentences = self.summarizer(self.parser.document, SENTENCES_COUNT)
        
        if(DEBUG):
            # print("DEBUG::ExtractivelySummarizeCorpus::these are all the parser.document.sentences")
            # print(self.parser.document.sentences)
            print("DEBUG::ExtractivelySummarizeCorpus::top n=%d sentences:"%SENTENCES_COUNT)
            for sentence in sentences:
                print(str(sentence))
        sentences = [str(sentence) for sentence in sentences]
        
        return sentences

    def ExtractTopics(self,sentences:List[str])->dict:
        
        TfidfVec = TfidfVectorizer(stop_words='english')

        tfidf = TfidfVec.fit_transform(sentences)
        features = TfidfVec.get_feature_names()

        if(DEBUG):
            print("DEBUG::ExtractTopics::all features (words)")
            print(features)

        cos_similarity_matrix = (tfidf * tfidf.T).toarray()
        dense_tfidf = tfidf.todense()

        if(DEBUG):
            print("DEBUG::ExtractTopics::tfidf matrix dimension:")
            print(tfidf.shape)
            print("DEBUG::ExtractTopics::dense tfidf matrix:")
            print(dense_tfidf)
            print("DEBUG::ExtractTopics::cos_similarity_matrix:")
            print(cos_similarity_matrix)

        topics = []
        all_importance_weights = np.empty(0)
        for i in np.arange(tfidf.shape[0]):
            for j in np.arange(tfidf.shape[0]):
                if((i!=j) and (cos_similarity_matrix[i,j]>0)):
                    importance_weights_vec = [dense_tfidf[i,k]*dense_tfidf[j,k] for k in np.arange(tfidf.shape[1])]
                    topic_indices = np.array(importance_weights_vec)>0
                    importance_weights = np.array(importance_weights_vec)[topic_indices]
                    tmp = np.array(features)[topic_indices]
                    topics.extend(list(tmp))
                    all_importance_weights = np.append(all_importance_weights,importance_weights)
                    if(DEBUG):
                        print(importance_weights)
                        print("DEBUG::ExtractTopics::extracted topics:")
                        print(tmp)
                        print("DEBUG::ExtractTopics::extracted topic weights:")
                        print(importance_weights)

        unique_topics = list(set(topics))   
        if(DEBUG):
            print("DEBUG::ExtractTopics::concatenated extracted topics:")
            print(topics)
            print("DEBUG::ExtractTopics::concatenated extracted topic weights:")
            print(all_importance_weights)
            print("DEBUG::ExtractTopics::unique extracted topics:")
            print(unique_topics)

        importance_weights = {}
        for topic in unique_topics:
            importance_weights[topic]=np.sum(all_importance_weights[np.array(topics)==topic])

        # normalize
        tmp = np.array(list(importance_weights.values()))
        # factor=1.0/sum(np.exp(tmp)) # useful if softmax is required
        importance_weights = {k: 1.0/(1.0+np.exp(-v)) for k, v in importance_weights.items() }
        # sort in decreasing order
        import operator
        sorted_importance_weights = sorted(importance_weights.items(), key=operator.itemgetter(1),reverse=True)
        
        return sorted_importance_weights

if __name__ == "__main__":
    url = "http://newknowledge.io/team"
    print("DEBUG::main::starting sumy url summarization test...")
    TopicExtractor = SubjectExplorer()
    sentences = TopicExtractor.ExtractivelySummarizeCorpus(url,True)
    extractedTopics = TopicExtractor.ExtractTopics(sentences)
    print("These are the extracted topics, from url: (sorted, importance weights included)")
    print(extractedTopics)
    filename = "data/6_20_17_32_bp_content.txt"
    #filename = "data/pro_gun_text.csv"
    print("DEBUG::main::starting sumy file summarization test...")
    TopicExtractor = SubjectExplorer()
    df = pd.read_csv(filename, dtype='str', header=None)
    # print(df)
    df_list = df.ix[0:MAX_N_ROWS,0].tolist()
    df_list = [sentence + '.' for sentence in df_list]
    # print(df_list)
    (pd.DataFrame(df_list)).to_csv("data/truncated_frame.csv",index=False)
    sentences = TopicExtractor.ExtractivelySummarizeCorpus("data/truncated_frame.csv",False)
    #sentences = df_list
    extractedTopics = TopicExtractor.ExtractTopics(sentences)
    print("These are the extracted topics, from file: (sorted, importance weights included)")
    print(extractedTopics)