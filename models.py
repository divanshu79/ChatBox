from __future__ import unicode_literals

from django.db import models

class user_data(models.Model):
    uid = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    password = models.CharField(max_length=250)

    def __str__(self):
        return self.uid
