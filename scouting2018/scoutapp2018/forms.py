from django import forms

class TeleopForm(forms.Form):
    times = forms.CharField(max_length = 10000)

class MatchEntryForm(forms.Form):
    match_number = forms.IntegerField()

class TeamEntryForm(forms.Form):
    team_number = forms.IntegerField()

class TeamLookupForm(forms.Form):
    team_number = forms.CharField()
