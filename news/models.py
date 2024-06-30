from django.db import models


# Create your models here.
class News(models.Model):
    title = models.TextField()
    published_at = models.DateTimeField("date published")
    link = models.TextField()
    short = models.TextField()
    body = models.TextField()
    thumbnail = models.TextField()

    class Meta:
        db_table = "news"  # Specify the custom table name

    def __str__(self):
        return self.title
