from django.db import models

class Hotel(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    star_rating = models.IntegerField()
    mobile_phone = models.IntegerField()
    site = models.URLField(null=True, blank=True)

    class Meta:
        db_table = 'Hotel'

    def __str__(self):
        return self.name
