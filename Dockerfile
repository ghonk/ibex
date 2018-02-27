FROM python:3.6

RUN mkdir /app

WORKDIR /app

COPY . /app/

RUN pip3 install https://github.com/oroszgy/spacy-hungarian-models/releases/download/hu_tagger_web_md-0.1.0/hu_tagger_web_md-0.1.0.tar.gz
RUN python3 -m spacy link hu_tagger_web_md hu
RUN python3 -m spacy download en
RUN pip3 install -r requirements.txt

CMD ["python3", "-u", "main.py"]
