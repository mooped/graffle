FROM python:2.7-slim

ADD requirements.txt /graffle/
WORKDIR /graffle

RUN pip install -r requirements.txt

ADD . /graffle/

CMD python app.py

EXPOSE 80
