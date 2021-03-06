import os
from flask import Flask, jsonify, request

app = Flask(__name__)

from EntityParser import EntityParser

nlp = EntityParser()


@app.route('/')
def homepage():
    return 'Entity Extraction Service'


@app.route('/private/entityExtraction')
def extract_entities():
    text = request.args.get('text')
    lang = request.args.get('lang')

    entities = nlp.extract_entities(text, lang)

    return jsonify(entities)


def main():
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', default=3001)))
    # app.run(debug=True)


if __name__ == '__main__':
    main()
