from django.urls import path
from . import views


urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('creating_game', views.create_game, name='creating_game'),
    path('wait_joining/<str:game_id>/<str:player_name>', views.wait_joining, name='wait_joining'),
    path('character_info/<str:game_id>/<str:player_name>', views.character_info, name='character_info'),
    path('team_makeup/<str:game_id>/<int:task_num>/<int:try_num>/<str:player_name>',
         views.make_up_team, name='team_makeup'),
    path('update_team_info/<str:game_id>/<int:task_num>/<int:try_num>/<str:player_name>/<int:team_size>',
         views.update_team_info, name='update_team_info'),
    path('team_makeup_vote/<str:game_id>/<int:task_num>/<int:try_num>/<str:player_name>',
         views.team_makeup_vote, name='team_makeup_vote'),
    path('waiting_team_vote/<str:game_id>/<int:task_num>/<int:try_num>',
         views.waiting_team_vote, name='waiting_team_vote'),
]
