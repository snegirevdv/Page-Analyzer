build:
	poetry install
	psql -a -d $(DATABASE_URL) -f database.sql

lint:
	poetry run flake8 page_analyzer

debug:
	poetry run flask --app page_analyzer.app:app --debug run

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:8000 page_analyzer:app
