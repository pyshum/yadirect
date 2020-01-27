from djongo import models

# Create your models here.


class APIData(models.Model):
    date = models.TextField()
    callerNumber = models.TextField()
    callTags = models.TextField()
    source = models.TextField()
    source_type = models.TextField()
    utmCampaign = models.TextField()
    utmContent = models.TextField()
    utmMedium = models.TextField()
    utmSource = models.TextField()
    utmTerm = models.TextField()
    location = models.TextField()
    communication_type = models.TextField()

    objects = models.DjongoManager()

    def __str__(self):
        return str(self.id)

