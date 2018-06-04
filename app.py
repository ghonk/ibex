'''Flask app for the entity extraction service Ibex'''
from flask import Flask, jsonify, request

from config import PORT, DEBUG
from entities import get_entities

app = Flask(__name__)


@app.route('/')
def homepage():
    return 'Entity Extraction Service'


@app.route('/entities', methods=['GET', 'POST'])
def request_entities():
    ''' Takes a post or get request with the text provided as a query string
    arg or a form field and returns a list of entities extracted from that
    text. If text is a list of strings it will return a list of lists of the
    extracted entities. 
    '''

    lang = request.values.get('lang', 'english')
    text = request.values.get('text')
    if not text:
        return 'You must provide text in the request, either as a querystring or form argument.'
    if isinstance(text, list):
        if text and not isinstance(text[0], str):
            return 'Text must be a string or list of strings.'
        entities = [get_entities(doc, lang) for doc in text]
    elif isinstance(text, str):
        entities = get_entities(text, lang)
    else:
        return 'Text must be a string or list of strings.'

    return jsonify(entities)


def main():
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)


if __name__ == '__main__':
    main()
