# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import CycleTime, Match

admin.site.register(CycleTime)
admin.site.register(Match)
