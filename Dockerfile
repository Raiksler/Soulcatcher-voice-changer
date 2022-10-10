FROM python:3

RUN pip install poetry
RUN apt update
RUN apt -y install ffmpeg

ADD . /Soulcatcher
WORKDIR /Soulcatcher
RUN mkdir temp
WORKDIR ./temp
RUN mkdir voice
RUN mkdir machine
WORKDIR /Soulcatcher
RUN poetry install

ENTRYPOINT poetry run python3 main.py
