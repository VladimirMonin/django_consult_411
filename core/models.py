from django.db import models

class Master(models.Model):
    first_name = models.CharField()
    last_name = models.CharField()
    middle_name = models.CharField()

