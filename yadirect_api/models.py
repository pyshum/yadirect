# from django.db import models
from djongo import models
# from django.contrib.postgres.fields import JSONField

from yadirect_api.models_base import BaseModel


# class ApiData(models.Model):
#     data = JSONField(verbose_name='Данные запроса', default=dict)


class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    class Meta:
        abstract = True


class Entry(models.Model):
    blog = models.EmbeddedField(
        model_container=Blog
    )

    headline = models.CharField(max_length=255)
    objects = models.DjongoManager()
