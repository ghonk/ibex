FROM python:3.6

RUN mkdir /app

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

RUN python3 -m spacy download en
RUN python3 -m spacy download es
RUN python3 -m nltk.downloader stopwords

COPY . /app/

CMD ["python3", "-u", "main.py"]
