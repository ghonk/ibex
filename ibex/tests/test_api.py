from flask import Flask, jsonify, request
from ..config import PORT, DEBUG
from ..preprocess import prep_text
from ..entities import get_entities
import requests


def test_api():
    pass
    # app = Flask(__name__)
    # app.run(debug=True)
    # app.run(host='0.0.0.0', port=PORT, debug=DEBUG)

    # print('making req')
    # res = requests.get('/entities')
    # print('request res:', res)
    # TODO not sure how to do this...
