FROM python:3-slim-buster

ENV PORT=8081

COPY ./src src
COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

CMD ["sh", "-c", "uvicorn src.app:app --reload --host 0.0.0.0 --port $PORT"]
