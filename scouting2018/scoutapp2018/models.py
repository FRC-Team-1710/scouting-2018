# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from scoutapp2018.choices import  *

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

    blue_one_scout = models.CharField(max_length = 35, default = 'none')
    blue_two_scout = models.CharField(max_length = 35, default = 'none')
    blue_three_scout = models.CharField(max_length = 35, default = 'none')
    red_one_scout = models.CharField(max_length = 35, default = 'none')
    red_two_scout = models.CharField(max_length = 35, default = 'none')
    red_three_scout = models.CharField(max_length = 35, default = 'none')

    def __unicode__(self):
        return 'Match ' + str(self.match_number)

class Auto(models.Model):
    match = models.IntegerField()
    team = models.IntegerField()
    baseline_crossed = models.BooleanField(default = False)
    starting_position = models.CharField(max_length=10000, choices=AUTO_START_CHOICES)
    cubes_in_switch = models.IntegerField()
    cubes_in_scale = models.IntegerField()
    cubes_in_vault = models.IntegerField()
    cubes_dropped = models.IntegerField()

class EndGame(models.Model):
    match = models.IntegerField()
    team = models.IntegerField()
    on_platform = models.BooleanField()
    climb_success = models.CharField(max_length=1000, choices=CLIMB_SUCCESS)
    assist = models.CharField(max_length=1000, choices=ASSIST)
