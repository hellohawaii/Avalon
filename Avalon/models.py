from django.db import models
import random

# Create your models here.


class Team:
    captain = []
    team_member = []
    supporters = []
    objectors = []
    supporter_num = 0
    objector_num = 0


class Task:
    team_try1 = Team()
    team_try2 = Team()
    team_try3 = Team()
    team_try4 = Team()
    team_try5 = Team()
    team_trys = [team_try1, team_try2, team_try3, team_try4, team_try5]
    final_team = Team()
    success_num = 0
    fail_num = 0


class AvalonGame(models.Model):
    game_id = models.IntegerField(default=0)
    assigned_characters = []
    remained_characters = ["Merlin", "Percival", "Loyal Servant of Arthur", "Morgana", "Assassin"]
    current_task = 0
    team_size = [2, 3, 2, 3, 3]
    task1 = Task()
    task2 = Task()
    task3 = Task()
    task4 = Task()
    task5 = Task()
    tasks = [task1, task2, task3, task4, task5]
    captain_before = random.randrange(0, 5)

    def __str__(self):
        return str(self.game_id)


class Player(models.Model):
    game = models.ForeignKey(AvalonGame, on_delete=models.CASCADE)
    player_name = models.CharField(max_length=200)
    character = models.CharField(max_length=200)

    def __str__(self):
        return self.player_name
