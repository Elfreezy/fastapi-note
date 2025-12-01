FROM python:3.13-alpine

WORKDIR /code

COPY requirements.txt /code/requirements.txt 

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev && pip install --upgrade -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0","--port", "8000"]
