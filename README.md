# Install

### 1. Use Docker

Make sure its installed first

`docker-compose up`

### 2. Migrate Database

To migrate database

`docker-compose exec web pipenv run python migrate.py`
