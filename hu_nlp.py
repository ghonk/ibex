# This is basically this, except changed to have the same API as spaCy:
# https://github.com/oroszgy/hunlp/blob/master/src/main/python/hunlp/__init__.py

import requests
import logging
import os

class Token:
    def __init__(self,
                 arcLabel: str,
                 entityType: str,
                 headId: int,
                 id: int,
                 lemma: str,
                 pos: str,
                 tagProperties: dict,
                 text: str):
        self.i = id
        self.text = text
        self.lemma = lemma
        self.tag = pos
        self.pos_ = pos
        self.tag_properties = tagProperties
        self.head = headId
        self.dep_ = arcLabel
        self.entity_type = entityType

    def __str__(self):
        return self.text

    def __repr__(self):
        return "Token({})".format(", ".join(
            ["{}={}".format(k, str(v)) for k, v in self.__dict__.items()]))


class Sentence:
    def __init__(self, tokens):
        self._tokens = tokens

    def __iter__(self):
        return iter(self._tokens)

    def __getitem__(self, index):
        return self._tokens[index]

    def __str__(self):
        return " ".join(str(tok) for tok in self._tokens)

    def __repr__(self):
        return "Sentence({})".format(
            ", ".join(repr(tok) for tok in self._tokens))


class Doc:
    def __init__(self, sentences):
        self._sentences = sentences
        tokens = []
        for sentence in sentences:
          for token in sentence:
            tokens.append(token)

        self._tokens = tokens

    def __iter__(self):
        return iter(self._tokens)

    def __getitem__(self, index):
        return self._sentences[index]

    def __str__(self):
        return " ".join(str(s) for s in self._sentences)

    def __repr__(self):
        return "Doc(\n\t{}\n)".format(
            "\n\t".join(repr(s) for s in self._sentences))

    @property
    def ents(self):
        ne = []
        for tok in self:
            if tok.entity_type != "O":
                ne.append(tok)
        return ne


class HuNlp(object):
    host = os.getenv('HUNGARY_HOST', default="http://localhost:9090")
    def __init__(self, host=host, endpoint="v1/annotate"):
        self._url = "{}/{}".format(host, endpoint)

    def __call__(self, text):
        try:
            result = requests.post(self._url, json={"text": text})
            data = result.json()
            if data:
                return Doc([
                    Sentence([Token(**t) for t in sent["tokens"]])
                    for sent in data["sentences"]
                ])
            else:
                logging.error("Empty response got for ''".format(text))
                logging.error(result)
        except Exception as e:
            logging.error("Could not parse '{}'".format(text))
            logging.error(e)