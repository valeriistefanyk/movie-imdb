import csv
from typing import Any, Optional
from django.core.management.base import BaseCommand, CommandParser
from apps.movie.models import Movie


class Command(BaseCommand):
    help = "Import movie from IMDB dataset"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("-f", "--file", type=str, required=True)
        parser.add_argument("--delimiter", type=str, default="\t")

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        file_name = options.get("file")
        print("file name:", file_name)
        print("Start creating movies...")
        with open(file_name, encoding="utf-8") as f:
            csv_data = csv.reader(f, delimiter=options.get("delimiter", "\t"))
            count = 0
            for row in csv_data:
                row_data = {
                    "imdb_id": row[0],
                    "title_type": row[1],
                    "name": row[2],
                    "is_adult": row[4] == "1",
                    "year": f"{row[5]}-01-01" if row[5] != "\\N" else None,
                    "genres": row[8].split(",") if row[8] != "\\N" else [],
                }
                if row_data["title_type"].lower() not in Movie.TitleChoices.values:
                    continue

                movie, created = Movie.objects.get_or_create(
                    imdb_id=row_data["imdb_id"], defaults=row_data
                )
                if not created:
                    Movie.objects.filter(imdb_id=movie.imdb_id).update(**row_data)
                count += 1
            print(f"Was created {count} movie entries")
