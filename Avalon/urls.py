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
    path('waiting_team_vote/<str:game_id>/<int:task_num>/<int:try_num>/<str:player_name>',
         views.waiting_team_vote, name='waiting_team_vote'),
    path('voting_for_tasks/<str:game_id>/<int:task_num>/<str:player_name>',
         views.vote_for_task, name='voting_for_tasks'),
    path('task_vote/<str:game_id>/<int:task_num>/<str:player_name>', views.task_vote, name='task_vote'),
    path('waiting_task_vote/<str:game_id>/<int:task_num>/<str:player_name>',
         views.waiting_task_vote, name='waiting_task_vote'),
    path('assassinate_vote/<str:game_id>/<str:player_name>', views.assassinate_vote, name='assassinate_vote'),
    path('assassinate_results/<str:game_id>', views.assassinate_results, name='assassinate_results')
]
