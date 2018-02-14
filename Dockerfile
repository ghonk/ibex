FROM python:3.6

RUN mkdir /app

WORKDIR /app

COPY . /app/

RUN pip3 install -r requirements.txt
RUN python3 -m spacy download en

CMD ["python3", "-u", "main.py"]
