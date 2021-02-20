FROM python:3.8-slim-buster

RUN apt-get install --upgrade && \
    apt-get install -y make

COPY app /app
COPY Makefile /Makefile

EXPOSE 9696 53000

ENTRYPOINT ["make", "run"]