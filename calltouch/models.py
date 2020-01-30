from djongo import models

from yadirect_api.models_base import BaseModel


class APIData(BaseModel):
    date = models.DateTimeField()
    callerNumber = models.TextField()
    callTags = models.TextField()
    source = models.TextField()
    utmSource = models.TextField()
    utmMedium = models.TextField()
    utmCampaign = models.TextField()
    utmContent = models.TextField()
    utmTerm = models.TextField()
    uniqueCall = models.TextField()

    objects = models.DjongoManager()

    def __str__(self):
        return str(self.id)
