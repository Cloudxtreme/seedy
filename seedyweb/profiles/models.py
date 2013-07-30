# coding=utf-8
from django.db import models
from django.contrib.auth.models import User

# Profiles
class Profile(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    desc = models.TextField()

    def __unicode__(self):
        return self.name
