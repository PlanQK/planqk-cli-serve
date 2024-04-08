FROM python:3.8-slim-buster

ENV PORT=8081

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

RUN mkdir src
COPY ./src src

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

CMD ["sh", "-c", "uvicorn src.app:app --reload --host 0.0.0.0 --port $PORT"]
