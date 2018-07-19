FROM python:2.7-slim

ENV TZ=Europe/London

ADD requirements.txt /graffle/
WORKDIR /graffle

RUN pip install -r requirements.txt
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ADD . /graffle/

CMD python app.py

EXPOSE 80
