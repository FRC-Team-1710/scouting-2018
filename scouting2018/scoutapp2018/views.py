# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from scoutapp2018.forms import TeleopForm, MatchEntryForm, TeamLookupForm, AutoForm
from scoutapp2018.models import CycleTime, Match, Auto
from django import forms
from django.http import HttpResponse, HttpResponseRedirect

def index(request):
    return render(request, "scoutapp2018/index.html")

def match_entry(request):
    if request.method == 'POST':
        form = MatchEntryForm(request.POST)
        if form.is_valid():
            match_number = form.cleaned_data['match_number']
            request.session['current_match'] = match_number
            return HttpResponseRedirect('/scout/team_select/')
    else:
        form = MatchEntryForm()

    return render(request, "scoutapp2018/match_entry.html", {'form' : form})

def team_select(request):
    match_number = request.session.get('current_match')
    matches = Match.objects.order_by('match_number')
    current_match = None
    teams_in_match = []

    for match in matches:
        if match.match_number == match_number:
            current_match = match

    teams_in_match.append(str(current_match.blue_one))
    teams_in_match.append(str(current_match.blue_two))
    teams_in_match.append(str(current_match.blue_three))
    teams_in_match.append(str(current_match.red_one))
    teams_in_match.append(str(current_match.red_two))
    teams_in_match.append(str(current_match.red_three))

    if str(current_match.blue_one) in request.POST:
        request.session['team'] = current_match.blue_one
        return HttpResponseRedirect('/scout/scout_auto/')
    elif str(current_match.blue_two) in request.POST:
        request.session['team'] = current_match.blue_two
        return HttpResponseRedirect('/scout/scout_auto/')
    elif str(current_match.blue_three) in request.POST:
        request.session['team'] = current_match.blue_three
        return HttpResponseRedirect('/scout/scout_auto/')
    elif str(current_match.red_one) in request.POST:
        request.session['team'] = current_match.red_one
        return HttpResponseRedirect('/scout/scout_auto/')
    elif str(current_match.red_two) in request.POST:
        request.session['team'] = current_match.red_two
        return HttpResponseRedirect('/scout/scout_auto/')
    elif str(current_match.red_three) in request.POST:
        request.session['team'] = current_match.red_three
        return HttpResponseRedirect('/scout/scout_auto/')

    context = {'match_number' : request.session.get('current_match'), 'teams' : teams_in_match}
    return render(request, "scoutapp2018/team_select.html", context)

def scout_auto(request):
    if request.method == 'POST':
        form = AutoForm(request.POST)
        if form.is_valid():
            new_auto = Auto(team=request.session.get('team'),
                            match=request.session.get('current_match'),
                            starting_position=form.cleaned_data['starting_position'],
                            cubes_in_switch=form.cleaned_data['cubes_in_switch'],
                            cubes_in_scale=form.cleaned_data['cubes_in_scale'],
                            cubes_in_vault=form.cleaned_data['cubes_in_vault'],
                            cubes_dropped=form.cleaned_data['cubes_dropped'])
            new_auto.save()
            return HttpResponseRedirect('/scout/scout_teleop/')
    else:
        form = AutoForm()

    context = {'form' : form}
    return render(request, "scoutapp2018/scout_auto.html", context)

def scout_teleop(request):
    if request.method == 'POST':
        form = TeleopForm(request.POST)
        if form.is_valid():
            #really icky, each cycle is seperated by ']', each location by ':' and each time by ','
            ugly_string_from_form = str(form.cleaned_data['times'])
            #a list containing each cycle, picked out of the raw form data
            cycles_raw = ugly_string_from_form.split("]")
            # a list containing the location of each cycle (switch/scale/dropped)
            cycle_locations = []
            # a list containing the times it took to complete each cycle
            cycle_times = []
            #contains formatted cycles to be saved
            cycles = []
            for cycle in cycles_raw:
                cycle_locations.append(cycle.split(":")[0])

            for time in cycles_raw:
                cycle_times.append(round(float(time.split(",")[1]), 2))

            for i in range(0,len(cycle_times)):
                cycles.append([cycle_times[i], cycle_locations[i]])
            #TODO: implement the team/match selection page and pass through current team and match, not 1710
            for cycle in cycles:
                new_cycle_time = CycleTime(time = cycle[0], team =request.session.get('team'), match=request.session.get('current_match'), location=cycle[1])
                new_cycle_time.save()

            return HttpResponseRedirect('/scout/')
    else:
        form = TeleopForm()

    return render(request, "scoutapp2018/scout_teleop.html", {'form' : form, 'match_number' : request.session.get('current_match'), 'team' : request.session.get('team')})

def team_lookup(request):
    if request.method == 'POST':
        form = TeamLookupForm(request.POST)

        if form.is_valid():
            team_number = form.cleaned_data['team_number']
            return team(request, str(team_number))

    else:
        form = TeamLookupForm()

    return render(request, "scoutapp2018/team_lookup.html", {'form' : form})

def team(request, team_number):
    cycle_times = CycleTime.objects.filter(team=team_number)
    autos = Auto.objects.filter(team=team_number)

    context = {'times': cycle_times, 'autos' : autos}
    return render(request, "scoutapp2018/team.html", context)
