from django.db import models
import random

# Create your models here.


class AvalonGame(models.Model):
    game_id = models.IntegerField(default=0)
    # assigned_characters = []
    # remained_characters = ["Merlin", "Percival", "Loyal Servant of Arthur", "Morgana", "Assassin"]
    # current_task = 0
    team_size = [2, 3, 2, 3, 3]
    # task1 = Task()
    # task2 = Task()
    # task3 = Task()
    # task4 = Task()
    # task5 = Task()
    success_tasks_num = models.IntegerField(default=0)
    fail_tasks_num = models.IntegerField(default=0)
    Assassin_success = models.BooleanField(default=False)
    Assassin_fail = models.BooleanField(default=False)
    # tasks = [task1, task2, task3, task4, task5]
    captain_before = models.IntegerField(default=random.randrange(0, 5))

    def __str__(self):
        return str(self.game_id)


class Player(models.Model):
    game = models.ForeignKey(AvalonGame, on_delete=models.CASCADE)
    player_name = models.CharField(max_length=200)
    character = models.CharField(max_length=200)

    def __str__(self):
        return self.player_name


class Task(models.Model):
    game = models.ForeignKey(AvalonGame, on_delete=models.CASCADE)
    success_num = models.IntegerField(default=0)
    fail_num = models.IntegerField(default=0)


class TryTeam(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    captain_name = models.CharField(max_length=200, default="")
    captain_num = models.IntegerField(default=6)
    supporter_num = models.IntegerField(default=0)
    objector_num = models.IntegerField(default=0)


class TryTeamMember(models.Model):
    player_name = models.CharField(max_length=200)
    team = models.ForeignKey(TryTeam, on_delete=models.CASCADE)


# class FinalTeam(models.Model):
#     task = models.ForeignKey(Task, on_delete=models.CASCADE)
#     captain_name = models.CharField(max_length=200, default="")


# class FinalTeamMember(models.Model):
#     player_name = models.CharField(max_length=200)
#     team = models.ForeignKey(FinalTeam, on_delete=models.CASCADE)


class TryTeamSupporter(models.Model):
    player_name = models.CharField(max_length=200)
    team = models.ForeignKey(TryTeam, on_delete=models.CASCADE)


class TryTeamObjector(models.Model):
    player_name = models.CharField(max_length=200)
    team = models.ForeignKey(TryTeam, on_delete=models.CASCADE)


class AssignedCharacter(models.Model):
    character = models.CharField(max_length=200)
    game = models.ForeignKey(AvalonGame, on_delete=models.CASCADE)


class RemainedCharacter(models.Model):
    character = models.CharField(max_length=200)
    game = models.ForeignKey(AvalonGame, on_delete=models.CASCADE)
