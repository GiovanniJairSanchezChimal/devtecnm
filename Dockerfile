FROM python:3.12-alpine3.20

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apk update \
    && apk add --no-cache gcc musl-dev mariadb-dev postgresql-dev python3-dev libffi-dev \
    && pip install --upgrade pip


COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./ ./

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "ventas_deliverysnk.wsgi:application"]
