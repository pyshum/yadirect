from djongo import models

# Create your models here.


class APIData(models.Model):
    campaign = models.TextField()
    date = models.TextField()
    medium = models.TextField()
    source = models.TextField()
    sessions = models.TextField()
    pageviews = models.TextField()
    adClicks = models.TextField()
    adCost = models.TextField()
    impressions = models.TextField()

    objects = models.DjongoManager()

    def __str__(self):
        return str(self.id)

