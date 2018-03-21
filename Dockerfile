FROM python:3.6

RUN mkdir /app

WORKDIR /app

COPY . /app/

RUN pip3 install -r requirements.txt
RUN python3 -m spacy download en
RUN python3 -m spacy download es_core_news_md

CMD ["python3", "-u", "main.py"]
