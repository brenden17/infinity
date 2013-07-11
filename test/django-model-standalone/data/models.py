from django.db import models

class Tweet(models.Model):
     text = models.CharField(max_length=255)
