from django import forms
from scoutapp2018.choices import *

class TeleopForm(forms.Form):
    times = forms.CharField(max_length = 10000)

class AutoForm(forms.Form):
    starting_position = forms.CharField(help_text= "Starting Position", max_length = 10000, widget=forms.Select(choices=AUTO_START_CHOICES))
    cubes_in_switch = forms.IntegerField(help_text= "Cubes in switch")
    cubes_in_scale = forms.IntegerField(help_text= "Cubes in scale")
    cubes_in_vault = forms.IntegerField(help_text= "Cubes in vault")
    cubes_dropped = forms.IntegerField(help_text= "Cubes dropped")

class EndGameForm(forms.Form):
    on_platform = forms.BooleanField(help_text="Are they on the platform?", required = False)
    climb_success = forms.CharField(help_text="rate their success in climbing", max_length=1000, widget=forms.Select(choices=CLIMB_SUCCESS))
    assist = forms.CharField(help_text="rate their ability to assist", max_length=1000, widget=forms.Select(choices=ASSIST))

class MatchEntryForm(forms.Form):
    match_number = forms.IntegerField()

class TeamEntryForm(forms.Form):
    team_number = forms.IntegerField()

class TeamLookupForm(forms.Form):
    team_number = forms.CharField()

class TeamMatchView(forms.Form):
    match_number = forms.IntegerField()

class ScoutLogin(forms.Form):
	username = forms.CharField(help_text="username", max_length=100, required = True)
	password = forms.CharField(help_text="password", max_length=100, required = True)

class ScoutRegister(forms.Form):
    scout_name = forms.CharField(help_text="username", max_length=100, required = True)
    scout_password = forms.CharField(help_text="password", max_length=100, required = True)
    scout_email = forms.CharField(help_text="email", max_length=100, required = True)
