# Movie IMDB
This project is intended to be an example of a django proj. It takes data from imdb and displays it.

## DEMO
[movie.phabious.store](movie.phabious.store "The IMDB movie data").


## Quickstart
- clone it
- run `cp .env.example .env` and fill it with your data
- run `docker-compose up`
- go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)


## Configuration
Project is configured through settings package

## Deployment
Project is automatically deployed via circle.ci

## Custom Management Commands
You can use custom management commands for fill in imdb movie data. There are 3 commands:
- run `./manage.py import_movies --file dataset/title.basics.tsv` to create movies
- run `./manage.py import_persons --file dataset/name.basics.tsv` to create persons
- run `./manage.py import_movieperson --file dataset/title.principals.tsv` to create intermediate table person-movie
