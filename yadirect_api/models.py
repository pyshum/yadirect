from django.db import models
from django.contrib.postgres.fields import JSONField

from yadirect_api.models_base import BaseModel


class ApiData(BaseModel):
    data = JSONField(verbose_name='Данные запроса', default=dict)
