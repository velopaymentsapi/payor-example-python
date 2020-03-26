FROM python:3.7-slim

ADD ./src /usr/src/app

WORKDIR /usr/src/app

RUN apt-get clean
RUN apt-get update
RUN apt-get install -y build-essential libpq-dev libpq5 git
RUN pip install --upgrade pip
RUN pip install pur
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get -y purge build-essential libpq-dev git
RUN apt-get autoremove -y
RUN apt-get clean

VOLUME /usr/src/app

CMD python run.py