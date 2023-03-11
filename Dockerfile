# https://fastapi.tiangolo.com/deployment/docker/
FROM python:3.11.2-slim as base

ENV TZ America/Toronto

FROM base as builder
WORKDIR /install

COPY requirements.txt /

RUN pip install --prefix=/install -r /requirements.txt

FROM base as prod
WORKDIR /usr/src/app

COPY --from=builder /install /usr/local
COPY . .

EXPOSE 80

ENTRYPOINT [ "python3" ]
CMD ["main.py"]
