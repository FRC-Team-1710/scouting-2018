# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class CycleTime(models.Model):
    time = models.DecimalField(max_digits=10, decimal_places=4)
    team = models.PositiveIntegerField()
    match = models.PositiveIntegerField()
    location = models.CharField(max_length = 35, default = 'none')

    def __unicode__(self):
	       return 'Team ' + str(self.team) + ' ' + str(self.location) + ' cycle'

class Match(models.Model):
    match_number = models.PositiveIntegerField()
    blue_one = models.PositiveIntegerField()
    blue_two = models.PositiveIntegerField()
    blue_three = models.PositiveIntegerField()
    red_one = models.PositiveIntegerField()
    red_two = models.PositiveIntegerField()
    red_three = models.PositiveIntegerField()

class Auto(models.Model):
