FROM python:3.6

ENV HOME=/app FLASK_APP=ibex/app.py

RUN mkdir /app \
    && pip install --upgrade pip 

COPY requirements.txt $HOME/

WORKDIR $HOME

RUN pip install -r requirements.txt \
    && python -c "import nltk; nltk.download('stopwords')" \
    && python -m spacy download en \
    && python -m spacy download es  

COPY . $HOME/

RUN python setup.py install

CMD ["flask", "run", "--host=0.0.0.0"]
