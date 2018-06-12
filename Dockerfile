FROM python:3.6-slim

RUN mkdir /app \
    && pip install --upgrade pip
# && apt-get update \
# && apt-get install -y --no-install-recommends gcc

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt 
RUN python -c "import nltk; nltk.download('stopwords')"
RUN python -m spacy download en \
    && python -m spacy download es

ENV FLASK_APP=ibex/app.py
CMD ["flask", "run", "--host=0.0.0.0"]