FROM python:3.11
WORKDIR /app

COPY pyproject.toml .
COPY Makefile .

RUN pip install --no-cache-dir poetry
RUN poetry install

COPY . .

EXPOSE 5001

CMD ["make", "start"]
