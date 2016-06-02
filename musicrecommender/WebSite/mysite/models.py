from django.db import models


class Artists(models.Model):
    id = models.IntegerField()
    name = models.TextField()
    tags = models.TextField()