from django.db import models


# Create your models here.
class Destination(models.Model):
    title = models.TextField()
    short = models.TextField()
    provinsi = models.TextField()
    kota = models.TextField()
    body = models.TextField()
    thumbnail = models.TextField()

    class Meta:
        db_table = "destinations"  # Specify the custom table name

    def __str__(self):
        return self.title
