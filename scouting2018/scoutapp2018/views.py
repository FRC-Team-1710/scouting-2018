# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from scoutapp2018.forms import TeleopForm, MatchEntryForm, TeamLookupForm, AutoForm, ScoutRegister, ScoutLogin, EndGameForm, TeamMatchView, MatchLookupForm
from scoutapp2018.models import CycleTime, Match, Auto, EndGame
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout as django_logout
import csv
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

import tbapy

def master_delete(request):
    CycleTime.objects.order_by('team').delete()
    Match.objects.order_by('team').delete()
    Auto.objects.order_by('team').delete()
    EndGame.objects.order_by('team').delete()
    return HttpResponse("hey")

def view_rank(request):
    #make a bunch of links at the top of the page and if you click on one it'll scroll you down to a table (using # in the url)
    autos = Auto.objects.order_by('cubes_in_scale')
    autos_success = Auto.objects.order_by('team')
    cycles = CycleTime.objects.order_by('team')
    teams_with_cube_in_scale = []
    teams_with_multiple_cube_autos = []
    teams = []
    auto_success_percent = []
    baseline_cross_success = []
    teleop_best_scale_match = []
    teleop_best_switch_match = []
    teleop_best_switch_block_match = []

    for auto in autos:
    	if auto.cubes_in_scale > 0:
	    teams_with_cube_in_scale.append([str(auto.team),str(auto.cubes_in_scale),str(auto.match)])

    for auto in autos:
        if auto.cubes_in_scale > 1 or (auto.cubes_in_switch > 1) or (auto.cubes_in_switch > 0 and auto.cubes_in_scale > 0):
            teams_with_multiple_cube_autos.append([str(auto.team), str(auto.match)])

    last_team = 0

    for auto in autos_success:
        team = auto.team
        if team != last_team:
            teams.append(team)
        last_team = team

    for team in teams:
        team_autos = autos_success.filter(team=team)
        successful = 0
        total = 0
        for auto in team_autos:
            if auto.cubes_in_switch > 0 or auto.cubes_in_scale > 0:
                successful += 1
            total += 1
        if total > 0 and successful > 0:
            auto_success_percent.append([team, round((float(successful)/float(total)), 3) * 100])

    auto_success_percent = sorted(auto_success_percent, key=lambda l:l[1], reverse=True)

    for team in teams:
        team_autos = autos.filter(team=team)

        successful = 0
        total = 0

        for auto in team_autos:
            if auto.baseline_crossed == True:
                successful += 1
            total+=1
        if total > 0:
            baseline_cross_success.append([team, round((float(successful)/float(total)), 3) * 100])

    baseline_cross_success = sorted(baseline_cross_success, key=lambda l:l[1], reverse=True)

    for team in teams:
        matches_played_by_team = []
        scale_cycles_by_match = []
        team_scale_cycles = cycles.filter(team=team).filter(location="Scale")
        last_match = 0
        for cycle in team_scale_cycles:
            match = cycle.match

            if match != last_match:
                matches_played_by_team.append(match)

            last_match = cycle.match

        for match in matches_played_by_team:
            team_scale_cycles = len(cycles.filter(team=team).filter(location="Scale").filter(match=match))
            scale_cycles_by_match.append([team_scale_cycles, match])

        scale_cycles_by_match = sorted(scale_cycles_by_match, key=lambda l:l[0], reverse=True)
        if len(scale_cycles_by_match) > 0:
            teleop_best_scale_match.append([team, scale_cycles_by_match[0][1], scale_cycles_by_match[0][0]])

    teleop_best_scale_match = sorted(teleop_best_scale_match, key=lambda l:l[2], reverse=True)

    for team in teams:
        matches_played_by_team = []
        switch_cycles_by_match = []
        team_switch_cycles = cycles.filter(team=team).filter(location="Switch")
        last_match = 0
        for cycle in team_switch_cycles:
            match = cycle.match

            if match != last_match:
                matches_played_by_team.append(match)

            last_match = cycle.match

        for match in matches_played_by_team:
            team_switch_cycles = len(cycles.filter(team=team).filter(location="Switch").filter(match=match))
            switch_cycles_by_match.append([team_switch_cycles, match])

        switch_cycles_by_match = sorted(switch_cycles_by_match, key=lambda l:l[0], reverse=True)
        if len(switch_cycles_by_match) > 0:
            teleop_best_switch_match.append([team, switch_cycles_by_match[0][1], switch_cycles_by_match[0][0]])

    teleop_best_switch_match = sorted(teleop_best_switch_match, key=lambda l:l[2], reverse=True)

    for team in teams:
        matches_played_by_team = []
        switch_blocks_by_match = []
        opp_switch_cycles = cycles.filter(team=team).filter(location="Opp-Switch")
        last_match = 0
        for cycle in opp_switch_cycles:
            match = cycle.match

            if match != last_match:
                matches_played_by_team.append(match)

            last_match = cycle.match

        for match in matches_played_by_team:
            opp_switch_cycles = len(cycles.filter(team=team).filter(location="Opp-Switch").filter(match=match))
            switch_blocks_by_match.append([opp_switch_cycles, match])

        switch_blocks_by_match = sorted(switch_blocks_by_match, key=lambda l:l[0], reverse=True)
        if len(switch_blocks_by_match) > 0:
            teleop_best_switch_block_match.append([team, switch_blocks_by_match[0][1], switch_blocks_by_match[0][0]])

    teleop_best_switch_block_match = sorted(teleop_best_switch_block_match, key=lambda l:l[2], reverse=True)

    context = {'scale_auto': teams_with_cube_in_scale,
	 'mult_cube_autos': teams_with_multiple_cube_autos,
	 'auto_success_percent' : auto_success_percent,
     'baseline_success_percent' : baseline_cross_success,
     'best_scale_matches' : teleop_best_scale_match,
     'best_switch_matches' : teleop_best_switch_match,
     'best_switch_blocks' : teleop_best_switch_block_match}
    return render(request, "scoutapp2018/rank.html", context)

def download_raw_auto(request):
    response_auto = HttpResponse(content_type='text/csv')
    response_auto['Content-Disposition'] = 'attachment; filename="kc_raw_auto.csv"'
    writer_auto = csv.writer(response_auto)

    autos = Auto.objects.order_by('match')

    writer_auto.writerow(['Match', 'Team', 'Baseline Crossed?', 'starting pos', 'cubes in switch',
			'cubes in scale', 'cubes in vault', 'cubes dropped'])
    for auto in autos:
        writer_auto.writerow([auto.match, auto.team, auto.baseline_crossed, auto.starting_position,
				 auto.cubes_in_switch, auto.cubes_in_scale, auto.cubes_in_vault,
				 auto.cubes_dropped])
    return response_auto

def download_raw_cycles(request):
    response_cycle = HttpResponse(content_type='text/csv')
    response_cycle['Content-Disposition'] = 'attachment; filename="kc_raw_cycle.csv"'

    writer_cycle = csv.writer(response_cycle)

    writer_cycle.writerow(['Match', 'Team', 'location', 'time'])
    cycles = CycleTime.objects.order_by('match')

    for cycle in cycles:
        writer_cycle.writerow([cycle.match, cycle.team, cycle.location, cycle.time])

    return response_cycle

def download_raw_end_game(request):
    response_end = HttpResponse(content_type='text/csv')
    response_end['Content-Disposition'] = 'attachment; filename="kc_raw_end.csv"'

    writer_end = csv.writer(response_end)

    writer_end.writerow(['Match', 'Team', 'on platform', 'success', 'assist'])
    endgames = EndGame.objects.order_by('match')

    for end in endgames:
        writer_end.writerow([end.match, end.team, end.on_platform, end.assist])

    return response_end

def index(request):
    context = {}
    if request.user.username:
        context = {'user' : request.user}
    else:
        context = {'user' : 42}
    return render(request, "scoutapp2018/index.html", context)

def scout_leaderboard(request):
    scout_list = []
    users = User.objects.order_by('username')
    scouts_matches = []
    matches = Match.objects.order_by('match_number')

    for user in users:
        scout_list.append(user.username)

    for scout in scout_list:
        r_one = len(matches.filter(red_one_scout=scout))
        r_two = len(matches.filter(red_two_scout=scout))
        r_three = len(matches.filter(red_three_scout=scout))
        b_one = len(matches.filter(blue_one_scout=scout))
        b_two = len(matches.filter(blue_two_scout=scout))
        b_three = len(matches.filter(blue_three_scout=scout))
        total_scouted = r_one + r_two + r_three + b_one + b_two + b_three
        scouts_matches.append([scout, total_scouted])

    scouts_matches = sorted(scouts_matches, key=lambda l:l[1], reverse=True)

    return render(request, "scoutapp2018/leaderboard.html", {'scouts' : scouts_matches})

def scout_register(request):
	if request.method == 'POST':
		form = ScoutRegister(request.POST)
		if form.is_valid():
			user = User.objects.create_user(form.cleaned_data['scout_name'], form.cleaned_data['scout_email'], form.cleaned_data['scout_password'])
			user.save()
			user = authenticate(username=form.cleaned_data['scout_name'], password=form.cleaned_data['scout_password'])
			if user is not None:
				login(request, user)
				return HttpResponseRedirect('/scout/')
			return index(request)
		else:
			print form.errors
	else:
		form = ScoutRegister()
	return render(request, 'scoutapp2018/register_scout.html', { 'form' : form})

def scout_login(request):
	if request.method == 'POST':
		form = ScoutLogin(request.POST)
		if form.is_valid():
			user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
			if user is not None:
				login(request, user)
				return HttpResponseRedirect('/scout/')
			else:
				return HttpResponse("login failed")
		else:
			print form.errors
	else:
		form = ScoutLogin()
	return render(request, 'scoutapp2018/scout_login.html', { 'form' : form })

@login_required
def logout(request):
	django_logout(request)
	return HttpResponseRedirect('/scout/')

@login_required
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

@login_required
def team_select(request):
    match_number = request.session.get('current_match')
    current_match = Match.objects.filter(match_number=match_number)[0]
    blue_teams = []
    red_teams = []
    teams_already_chosen = []
    errors = []

    scouts_in_match = [current_match.blue_one_scout,current_match.blue_two_scout,current_match.blue_three_scout,
                        current_match.red_one_scout, current_match.red_two_scout, current_match.red_three_scout]

    blue_teams.append(str(current_match.blue_one))
    blue_teams.append(str(current_match.blue_two))
    blue_teams.append(str(current_match.blue_three))
    red_teams.append(str(current_match.red_one))
    red_teams.append(str(current_match.red_two))
    red_teams.append(str(current_match.red_three))

    if scouts_in_match[0] != 'none':
        teams_already_chosen.append(blue_teams[0])
    if scouts_in_match[1] != 'none':
        teams_already_chosen.append(blue_teams[1])
    if scouts_in_match[2] != 'none':
        teams_already_chosen.append(blue_teams[2])
    if scouts_in_match[3] != 'none':
        teams_already_chosen.append(red_teams[0])
    if scouts_in_match[4] != 'none':
        teams_already_chosen.append(red_teams[1])
    if scouts_in_match[5] != 'none':
        teams_already_chosen.append(red_teams[2])

    if str(current_match.blue_one) in request.POST and (current_match.blue_one_scout == 'none' or current_match.blue_one_scout == request.user.username):
        current_match.blue_one_scout = request.user.username
        current_match.save()
        request.session['team'] = current_match.blue_one
        return HttpResponseRedirect('/scout/scout_auto/')
    elif str(current_match.blue_two) in request.POST and (current_match.blue_two_scout == 'none' or current_match.blue_two_scout == request.user.username):
        current_match.blue_two_scout = request.user.username
        current_match.save()
        request.session['team'] = current_match.blue_two
        return HttpResponseRedirect('/scout/scout_auto/')
    elif str(current_match.blue_three) in request.POST and (current_match.blue_three_scout == 'none' or current_match.blue_three_scout == request.user.username):
        current_match.blue_three_scout = request.user.username
        current_match.save()
        request.session['team'] = current_match.blue_three
        return HttpResponseRedirect('/scout/scout_auto/')
    elif str(current_match.red_one) in request.POST and (current_match.red_one_scout == 'none' or current_match.red_one_scout == request.user.username):
        current_match.red_one_scout = request.user.username
        current_match.save()
        request.session['team'] = current_match.red_one
        return HttpResponseRedirect('/scout/scout_auto/')
    elif str(current_match.red_two) in request.POST and (current_match.red_two_scout == 'none' or current_match.red_two_scout == request.user.username):
        current_match.red_two_scout = request.user.username
        current_match.save()
        request.session['team'] = current_match.red_two
        return HttpResponseRedirect('/scout/scout_auto/')
    elif str(current_match.red_three) in request.POST and (current_match.red_three_scout == 'none' or current_match.red_three_scout == request.user.username):
        current_match.red_three_scout = request.user.username
        current_match.save()
        request.session['team'] = current_match.red_three
        return HttpResponseRedirect('/scout/scout_auto/')
    else:
        errors.append("Please Select a Team ")

    context = {'match_number' : request.session.get('current_match'), 'blue_teams' : blue_teams, 'red_teams' : red_teams, 'errors' : errors, 'selected_teams' : teams_already_chosen}
    return render(request, "scoutapp2018/team_select.html", context)

@login_required
def scout_auto(request):
    if request.method == 'POST':
        form = AutoForm(request.POST)
        if form.is_valid():
            new_auto = Auto(team=request.session.get('team'),
                            match=request.session.get('current_match'),
                            baseline_crossed=form.cleaned_data['baseline_crossed'],
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

@login_required
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

            return HttpResponseRedirect('/scout/scout_end')
    else:
        form = TeleopForm()

    return render(request, "scoutapp2018/scout_teleop.html", {'form' : form, 'match_number' : request.session.get('current_match'), 'team' : request.session.get('team')})

@login_required
def scout_end(request):
    if request.method == 'POST':
        form = EndGameForm(request.POST)
        if form.is_valid():
            new_end_game = EndGame(match=request.session.get('current_match'),
                                   team=request.session.get('team'),
                                   on_platform=form.cleaned_data['on_platform'],
                                   climb_success=form.cleaned_data['climb_success'],
                                   assist=form.cleaned_data['assist'])
            new_end_game.save()
            return HttpResponseRedirect('/scout/')
    else:
        form = EndGameForm()

    context = {'form' : form}
    return render(request, "scoutapp2018/scout_end.html", context)

#thanks Corey!!!
def load_match_list(request):
    #use arkansas for testing but change to heartland later
    event = "2018iacf"
    tba = tbapy.TBA("jwEmVymeOvhRakjCQWJS4sE4GHxD4TBKhXVsgtTtqLPvODraEbRtYz3YlmhddAkD")
    matchObjects = tba.event_matches(event, simple=True)
    master_schedule = []

    for match_ew in matchObjects:
        # Create the match list
        match = creatematchdata(match_ew)
        matchlevel = getattr(match_ew, "comp_level")
        if 'qm' not in matchlevel:
            print matchlevel
        else:
            new_match = Match(match_number=match[0],
                          blue_one=match[1],
                          blue_two=match[2],
                          blue_three=match[3],
                          red_one=match[4],
                          red_two=match[5],
                          red_three=match[6])
            new_match.save()

            # Write out the data to a dictionary to be used
            master_schedule.append(match)

    return render(request, "scoutapp2018/load_match_list.html")

def creatematchdata(matchtoeval):
    blue = "blue"
    red = "red"
    teamKeys = "team_keys"

    matchnumber = getattr(matchtoeval, "match_number")
    # Set up alliance dictionaries
    alliances = getattr(matchtoeval, "alliances")

    # Get teams that play on each alliance. There is a better way to do this, I just don't know what it is.
    blueteam1 = alliances[blue][teamKeys][0]
    blueteam2 = alliances[blue][teamKeys][1]
    blueteam3 = alliances[blue][teamKeys][2]
    redteam1 = alliances[red][teamKeys][0]
    redteam2 = alliances[red][teamKeys][1]
    redteam3 = alliances[red][teamKeys][2]
    # Trim teams down to just numbers since they are all formatted as 'frcXXXX'
    b1number = blueteam1[3:]
    b2number = blueteam2[3:]
    b3number = blueteam3[3:]
    r1number = redteam1[3:]
    r2number = redteam2[3:]
    r3number = redteam3[3:]

    # Create a list for the data of each match
    matchlist = [matchnumber, b1number, b2number, b3number,
                 r1number, r2number, r3number]

    return matchlist

@login_required
def team_lookup(request):
    if request.method == 'POST':
        form = TeamLookupForm(request.POST)

        if form.is_valid():
            team_number = form.cleaned_data['team_number']
            return team(request, str(team_number))

    else:
        form = TeamLookupForm()

    return render(request, "scoutapp2018/team_lookup.html", {'form' : form})

@login_required
def match_lookup(request):
    if request.method == "POST":
        form = MatchLookupForm(request.POST)

        if form.is_valid():
            return match(request, form.cleaned_data['match_number'])
    else:
        form = MatchLookupForm()

    return render(request, "scoutapp2018/match_lookup.html", {'form' : form})

@login_required
def match(request, match_number):
    match = Match.objects.filter(match_number=match_number)
    context = {'match_number' : match_number, 'match' : match}
    return render(request, "scoutapp2018/match.html", context)

@login_required
def team(request, team_number):
    cycle_times = CycleTime.objects.filter(team=team_number)
    autos = Auto.objects.filter(team=team_number)
    end_games = EndGame.objects.filter(team=team_number)

    tele_cubes_in_switch = len(CycleTime.objects.filter(team=team_number).filter(location="Switch"))
    tele_cubes_in_scale = len(CycleTime.objects.filter(team=team_number).filter(location="Scale"))
    tele_cubes_dropped = len(CycleTime.objects.filter(team=team_number).filter(location="Drop"))
    tele_cubes_in_exchange = len(CycleTime.objects.filter(team=team_number).filter(location="Exchange"))
    tele_cubes_in_opp_switch = len(CycleTime.objects.filter(team=team_number).filter(location="Opp-Switch"))

    switch_cycles = CycleTime.objects.filter(team=team_number).filter(location="Switch")
    scale_cycles = CycleTime.objects.filter(team=team_number).filter(location="Scale")
    exchange_cycles = CycleTime.objects.filter(team=team_number).filter(location="Exchange")

    switch_times = []
    scale_times = []
    exchange_times = []

    for cycle in switch_cycles:
        switch_times.append(cycle.time)

    for cycle in scale_cycles:
        scale_times.append(cycle.time)

    for cycle in exchange_cycles:
        exchange_times.append(cycle.time)

    avg_switch_time = 0
    avg_scale_time = 0
    avg_exchange_time = 0

    if tele_cubes_in_switch != 0:
        avg_switch_time = sum(switch_times)/tele_cubes_in_switch

    if tele_cubes_in_scale != 0:
        avg_scale_time = sum(scale_times)/tele_cubes_in_scale

    if tele_cubes_in_exchange != 0:
        avg_exchange_time = sum(exchange_times)/tele_cubes_in_exchange

    if request.method == 'POST':
        form = TeamMatchView(request.POST)

        if form.is_valid():
            match = form.cleaned_data['match_number']
            cycle_times = CycleTime.objects.filter(team=team_number).filter(match=match)
            autos = Auto.objects.filter(team=team_number).filter(match=match)
            end_games = EndGame.objects.filter(team=team_number).filter(match=match)
            tele_cubes_in_switch = len(CycleTime.objects.filter(team=team_number).filter(location="Switch").filter(match=match))
            tele_cubes_in_scale = len(CycleTime.objects.filter(team=team_number).filter(location="Scale").filter(match=match))
            tele_cubes_dropped = len(CycleTime.objects.filter(team=team_number).filter(location="Drop").filter(match=match))
            tele_cubes_in_exchange = len(CycleTime.objects.filter(team=team_number).filter(location="Exchange").filter(match=match))
    else:
        form = TeamMatchView(request.POST)

    climb_count = len(EndGame.objects.filter(team=team_number).filter(climb_success=u"succsessful"))
    assisted_count = len(EndGame.objects.filter(team=team_number).filter(climb_success=u"carried by another team"))
    levitate_count = len(EndGame.objects.filter(team=team_number).filter(climb_success=u"levitated"))
    fall_count = len(EndGame.objects.filter(team=team_number).filter(climb_success=u"fell"))
    no_attempt_count = len(EndGame.objects.filter(team=team_number).filter(climb_success=u"DNA"))

    on_platform = len(EndGame.objects.filter(team=team_number).filter(on_platform=True))
    not_on_platform = len(EndGame.objects.filter(team=team_number).filter(on_platform=False))

    data_for_charts = [tele_cubes_in_switch, tele_cubes_in_scale, tele_cubes_dropped, tele_cubes_in_exchange, avg_switch_time,
                       avg_scale_time, avg_exchange_time, climb_count, assisted_count, levitate_count, fall_count, no_attempt_count,
                       on_platform, not_on_platform, tele_cubes_in_opp_switch]

    context = {'times': cycle_times, 'autos' : autos, 'end_games' : end_games, 'chart_data' : data_for_charts, "form" : form, "team" : team_number}
    return render(request, "scoutapp2018/team.html", context)
