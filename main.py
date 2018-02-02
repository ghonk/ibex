import os
from flask import Flask, jsonify, request

app = Flask(__name__)

from EntityParser import EntityParser

nlp = EntityParser()

@app.route('/private/entityExtraction')
def extract_entities():
    text = request.args.get('text')
    entities = nlp.extractEntities(text).tolist()
    nouns = list(map(lambda e: e[0], entities))

    return jsonify(nouns)


def main():
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', default=3000)))


if __name__ == '__main__':
    main()
