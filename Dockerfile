FROM python:3.6

RUN mkdir /app \
    && pip install --upgrade pip 

WORKDIR /app
COPY . /app

RUN python setup.py install \
    && python -c "import nltk; nltk.download('stopwords')" \
    && python -m spacy download en \
    && python -m spacy download es  

ENV FLASK_APP=ibex/app.py
CMD ["flask", "run", "--host=0.0.0.0"]