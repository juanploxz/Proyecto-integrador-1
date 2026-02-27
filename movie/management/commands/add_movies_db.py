import json
import os

from django.core.management.base import BaseCommand
from movie.models import Movie


class Command(BaseCommand):
    help = "Carga 100 películas desde movies.json a la base de datos."

    def handle(self, *args, **options):
        base_dir = os.path.dirname(__file__)  # .../movie/management/commands
        json_path = os.path.join(base_dir, "movies.json")

        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f"No existe: {json_path}"))
            return

        with open(json_path, "r", encoding="utf-8") as f:
            movies = json.load(f)

        default_image_path = "movie/images/default.jpg"  # relativo a MEDIA_ROOT

        created = 0
        limit = 100

        for item in movies[:limit]:
            title = (item.get("title") or "").strip()
            if not title:
                continue

            # year viene como string en el dataset
            raw_year = item.get("year")
            year = None
            if raw_year is not None:
                try:
                    year = int(str(raw_year).strip())
                except ValueError:
                    year = None

            genre = (item.get("genre") or "").strip()

            # usa 'plot' como descripción (si no existe, cae a vacío)
            description = (item.get("plot") or item.get("description") or "").strip()

            # Evita duplicados básicos (title + year)
            exists = Movie.objects.filter(title=title, year=year).exists()
            if exists:
                continue

            m = Movie(
                title=title,
                year=year,
                genre=genre,
                description=description,
                url=item.get("poster") or item.get("url") or "",
            )

            # Asigna imagen por defecto
            m.image = default_image_path
            m.save()

            created += 1

        self.stdout.write(self.style.SUCCESS(f"Listo. Creadas: {created} películas (máx {limit})."))