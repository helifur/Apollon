FROM python:3.11

COPY . .

RUN poetry install

CMD ["uvicorn", "app.main:main", "--reload"]
