from django.db import models

# Create your models here.
# python manage.py makemigrations
# python manage.py  migrate

class Record(models.Model):
    En = models.CharField(max_length=255)
    timestamp = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    time = models.CharField(max_length=255)