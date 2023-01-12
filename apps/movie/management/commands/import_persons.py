import csv
from typing import Any, Optional
from django.core.management.base import BaseCommand, CommandParser
from apps.movie.models import Person


class Command(BaseCommand):
    help = "Import person from IMDB dataset"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("-f", "--file", type=str)
        parser.add_argument("--delimiter", type=str, default="\t")

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        file_name = options.get("file")
        print("Start creating persons...")
        with open(file_name, encoding="utf-8") as f:
            csv_data = csv.reader(f, delimiter=options.get("delimiter", "\t"))
            count = 0
            for row in csv_data:
                row_data = {
                    "imdb_id": row[0],
                    "name": row[1],
                    "birth_year": f"{row[2]}-01-01" if row[2] != "\\N" else None,
                    "death_year": f"{row[3]}-12-31" if row[3] != "\\N" else None,
                }

                person, created = Person.objects.get_or_create(
                    imdb_id=row_data["imdb_id"], defaults=row_data
                )
                if not created:
                    Person.objects.filter(imdb_id=person.imdb_id).update(**row_data)
                count += 1
            print(f"Was created {count} person entries")
