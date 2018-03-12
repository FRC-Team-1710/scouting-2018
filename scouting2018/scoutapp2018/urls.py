from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^view_rank/$', views.view_rank, name='view_rank'),
    url(r'^download_raw_auto/$', views.download_raw_auto, name='download_raw_auto'),
    url(r'^download_raw_cycles/$', views.download_raw_cycles, name='download_raw_cycles'),
    url(r'^download_raw_end_game/$', views.download_raw_end_game, name='download_raw_end_game'),
    url(r'^match_entry/$', views.match_entry, name='match_entry'),
    url(r'^team_select/$', views.team_select, name='team_select'),
    url(r'^scout_auto/$', views.scout_auto, name='scout_auto'),
    url(r'^scout_login/$', views.scout_login, name='scout_login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^scout_register/$', views.scout_register, name='scout_register'),
    url(r'^scout_teleop/$', views.scout_teleop, name='scout_teleop'),
    url(r'^scout_end/$', views.scout_end, name='scout_end'),
    url(r'^team_lookup/$', views.team_lookup, name='team_lookup'),
    url(r'^match_lookup/$', views.match_lookup, name='match_lookup'),
    url(r'^load_match_list/$', views.load_match_list, name='load_match_list'),
    url(r'^team/(?P<team_number>[0-9999]+)/$', views.team, name='team'),
    url(r'^match/(?P<match_number>[0-9999]+)/$', views.match, name='match'),
]
