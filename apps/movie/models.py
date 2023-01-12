from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField


class Movie(models.Model):
    imdb_id = models.CharField(_("IMDB id"), max_length=80)

    class TitleChoices(models.TextChoices):
        SHORT = ("short", _("Short Movie"))
        MOVIE = ("movie", _("Movie"))

    title_type = models.CharField(
        _("Title Type"), max_length=80, choices=TitleChoices.choices
    )
    name = models.CharField(_("Name"), max_length=255)
    is_adult = models.BooleanField(_("Is Adult"), default=False)
    year = models.DateField(_("Year"), null=True, blank=True)
    genres = ArrayField(models.CharField(_("Genres"), max_length=80))

    def __str__(self):
        return f"{self.name}"


class Person(models.Model):
    imdb_id = models.CharField(_("IMDB id"), max_length=80)
    name = models.CharField(_("Name"), max_length=255)
    birth_year = models.DateField(_("Birth Year"), blank=True, null=True)
    death_year = models.DateField(_("Death Year"), blank=True, null=True)

    def __str__(self):
        return f"{self.name}"


class PersonMovie(models.Model):
    person_id = models.ForeignKey("Person", on_delete=models.PROTECT)
    movie_id = models.ForeignKey("Movie", on_delete=models.PROTECT)

    order = models.IntegerField(_("Order"))
    category = models.CharField(_("Category"), max_length=80, null=True, blank=True)
    job = models.CharField(_("Job"), max_length=255, null=True, blank=True)
    characters = ArrayField(models.CharField(_("Characters"), max_length=255))

    def __str__(self):
        return f"{self.person_id} - {self.movie_id}"
