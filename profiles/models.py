# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class DateTimeBase(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Location(DateTimeBase):
    name = models.CharField(max_length=100)
    lat = models.DecimalField(decimal_places=6, max_digits=10)
    lng = models.DecimalField(decimal_places=6, max_digits=10)

    def __str__(self):
        return self.name

class UserProfile(DateTimeBase):
    user = models.ForeignKey(User)
    location = models.ForeignKey(Location)
    contact = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '%s-%s' % (self.user.username, self.location.name)

class PanditProfile(DateTimeBase):
    user = models.ForeignKey(User)
    location = models.ManyToManyField(Location)
    contact = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '%s' % (self.user.username)