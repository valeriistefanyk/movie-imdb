import csv
from typing import Any, Optional
from django.core.management.base import BaseCommand, CommandParser
from apps.movie.models import Person, Movie, PersonMovie


class Command(BaseCommand):
    help = "Import movie-person from IMDB dataset"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("-f", "--file", type=str, required=True)
        parser.add_argument("--delimiter", type=str, default="\t")

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        file_name = options.get("file")
        print("Start creating person-movies...")
        with open(file_name, encoding="utf-8") as f:
            csv_data = csv.reader(f, delimiter=options.get("delimiter", "\t"))
            count = 0
            for row in csv_data:
                try:
                    person = Person.objects.get(imdb_id=row[2])
                    movie = Movie.objects.get(imdb_id=row[0])
                except Person.DoesNotExist:
                    print(
                        f"Skip entry because person with imdb id {row[2]} does not exist in DB"
                    )
                    continue
                except Movie.DoesNotExist:
                    print(
                        f"Skip entry because movie with imdb id {row[0]} does not exist in DB"
                    )
                    continue
                row_data = {
                    "person_id": person,
                    "movie_id": movie,
                    "order": int(row[1]),
                    "category": row[3] if row[3] != "\\N" else None,
                    "job": row[4] if row[4] != "\\N" else None,
                    "characters": row[5].strip("][").split(", ")
                    if row[5] != "\\N"
                    else [],
                }
                person_movie, created = PersonMovie.objects.get_or_create(
                    person_id=row_data["person_id"],
                    movie_id=row_data["movie_id"],
                    defaults=row_data,
                )
                if not created:
                    PersonMovie.objects.filter(id=person_movie.id).update(**row_data)
                count += 1

            print(f"Was created {count} person-movie entries")
