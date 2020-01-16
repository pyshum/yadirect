# from django.db import models
from djongo import models
# from django.contrib.postgres.fields import JSONField

from yadirect_api.models_base import BaseModel


# class ApiData(models.Model):
#     data = JSONField(verbose_name='Данные запроса', default=dict)


class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Entry(models.Model):
    # blog = models.EmbeddedField(
    #     model_container=Blog
    # )
    # tagline = models.TextField()
    Date = models.TextField()
    CampaignId = models.TextField()
    Clicks = models.TextField()
    Cost = models.TextField()

    # headline = models.CharField(max_length=255)
    objects = models.DjongoManager()

    def __str__(self):
        return str(self.id)


# class CallTouchResponse(models.Model):
#     date = models.TextField()
#     callUrl = models.TextField()
#     uniqueCall = models.TextField()
#     callReferenceId = models.TextField()
#     utmContent = models.TextField()
#     source = models.TextField()
#     ref = models.TextField()
#     additionalTags = models.TextField()
#     hostname = models.TextField()
#     waitingConnect = models.TextField()
#     ctCallerId = models.TextField()
#     keyword = models.TextField()
#     callClientUniqueId = models.TextField()
#     order = models.TextField()
#     callTags = models.TextField()
#     utmSource = models.TextField()
#     sipCallId = models.TextField()
#     ip = models.TextField()
#     utmCampaign = models.TextField()
#     attrs = models.TextField()
#     phoneNumber = models.TextField()
#     uniqTargetCall = models.TextField()
#     utmMedium = models.TextField()
#     orders = models.TextField()
#     device = models.TextField()
#     sessionDate = models.TextField()
#     city = models.TextField()
#     redirectNumber = models.TextField()
#     siteName = models.TextField()
#     yaClientId = models.TextField()
#     medium = models.TextField()
#     callphase = models.TextField()
#     duration = models.TextField()
#     browser = models.TextField()
#     callbackCall = models.TextField()
#     successful = models.TextField()
#     timestamp = models.TextField()
#     callId = models.TextField()
#     clientId = models.TextField()
#     callerNumber = models.TextField()
#     os = models.TextField()
#     manager = models.TextField()
#     utmTerm = models.TextField()
#     userAgent = models.TextField()
#     sessionId = models.TextField()
#     url = models.TextField()
#     targetCall = models.TextField()
#     attribution = models.TextField()
#     siteId = models.TextField()
