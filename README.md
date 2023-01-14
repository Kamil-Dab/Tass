# TASS

### To start and build an application run:
```
docker compose up --build
```
Application will be available on http://localhost:8080

### In order to fill database with data run:
```
docker-compose run --rm web python initial_db.py
```
Data filling script might crash, because of not enought RAM available. In that case limit batch size
of flights saved in one transaction by changing `limit_bulk` variable in `initial_db.py` file.
