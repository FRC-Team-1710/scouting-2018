# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import CycleTime, Match, Auto, EndGame

admin.site.register(CycleTime)
admin.site.register(Match)
admin.site.register(Auto)
admin.site.register(EndGame)
