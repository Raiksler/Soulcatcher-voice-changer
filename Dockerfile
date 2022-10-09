FROM python:3

RUN pip install poetry
RUN apt update
RUN apt -y install ffmpeg

ADD . /Soulcatcher
WORKDIR /Soulcatcher
RUN poetry install

ENTRYPOINT poetry run python3 main.py
