from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^match_entry/$', views.match_entry, name='match_entry'),
    url(r'^team_select/$', views.team_select, name='team_select'),
    url(r'^scout_auto/$', views.scout_auto, name='scout_auto'),
    url(r'^scout_login/$', views.scout_login, name='scout_login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^scout_register/$', views.scout_register, name='scout_register'),
    url(r'^scout_teleop/$', views.scout_teleop, name='scout_teleop'),
    url(r'^scout_end/$', views.scout_end, name='scout_end'),
    url(r'^team_lookup/$', views.team_lookup, name='team_lookup'),
    url(r'^load_match_list/$', views.load_match_list, name='load_match_list'),
    url(r'^team/(?P<team_number>[0-9999]+)/$', views.team, name='team'),
]
