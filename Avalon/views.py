from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from Avalon.models import AvalonGame, Task, TryTeam
import random


# Create your views here.
def welcome(request):
    return render(request, 'Avalon/welcome.html')


def create_game(request):
    game_id = request.POST['game_id']
    player_name = request.POST['user_name']
    try:
        game = AvalonGame.objects.get(game_id=game_id)
    except AvalonGame.DoesNotExist:
        game = AvalonGame.objects.create(game_id=game_id)
        game.remainedcharacter_set.create(character="Merlin")
        game.remainedcharacter_set.create(character="Percival")
        game.remainedcharacter_set.create(character="Loyal Servant of Arthur")
        game.remainedcharacter_set.create(character="Morgana")
        game.remainedcharacter_set.create(character="Assassin")
    # print(game.remained_characters)
    random_character_num = game.remainedcharacter_set.count()
    random_character_i = random.randrange(0, random_character_num)
    random_character = game.remainedcharacter_set.all()[random_character_i].character
    game.assignedcharacter_set.create(character=random_character)
    game.remainedcharacter_set.all()[random_character_i].delete()
    # print(game.remained_characters)
    game.player_set.create(player_name=player_name, character=random_character)
    return HttpResponseRedirect(reverse('wait_joining', args=[game_id, player_name]))


def wait_joining(request, game_id, player_name):
    game = AvalonGame.objects.get(game_id=game_id)
    if game.player_set.all().count() < 5:
        return render(request, 'Avalon/wait_joining.html')
    else:
        return HttpResponseRedirect(reverse('character_info', args=[game_id, player_name]))


def character_info(request, game_id, player_name):
    character = AvalonGame.objects.get(game_id=game_id).player_set.get(player_name=player_name).character
    character_intro = get_character_intro(game_id, character)
    context = {'player_name': player_name, 'character': character, 'character_intro': character_intro,
               'game_id': game_id, 'task_num': 1, 'try_num': 1}
    return render(request, 'Avalon/character_info.html', context)


def get_character_intro(game_id, player_character):
    # "Merlin", "Percival", "Loyal Servant of Arthur", "Morgana", "Assassin"
    Merlin_player = get_character_player(game_id, 'Merlin')
    Percival_player = get_character_player(game_id, 'Percival')
    Loyal_player = get_character_player(game_id, 'Loyal Servant of Arthur')
    Morgana_player = get_character_player(game_id, 'Morgana')
    Assassin_player = get_character_player(game_id, 'Assassin')
    Merlin_and_Morgan = random.sample([Merlin_player, Morgana_player], k=2)
    intro = dict()
    intro['Merlin'] = 'You knows who are wicked people, %s and %s are wicked' % (Morgana_player, Assassin_player)
    intro['Percival'] = 'You knows one of %s and %s is Merlin and the other is Morgana' % \
                        (Merlin_and_Morgan[0], Merlin_and_Morgan[1])
    intro['Loyal Servant of Arthur'] = 'You do not have additional information.'
    intro['Morgana'] = 'You knows %s is Assassin' % Assassin_player
    intro['Assassin'] = 'You knows %s is Morgana' % Morgana_player
    return intro[player_character]


def get_character_player(game_id, character_name):
    return AvalonGame.objects.get(game_id=game_id).player_set.get(character=character_name).player_name


def make_up_team(request, game_id, task_num, try_num, player_name):
    current_game = AvalonGame.objects.get(game_id=game_id)
    try:
        current_task = current_game.task_set.all()[task_num-1]
    except IndexError:
        current_task = current_game.task_set.create()
    try:
        current_try = current_task.tryteam_set.all()[try_num-1]
    except IndexError:
        current_try = current_task.tryteam_set.create()
    # use index of player to represent the captain
    if current_try.captain_name == "":
        # choose a captain when the first user want to make up a team
        current_captain_num = (current_game.captain_before + 1) % 5
        current_try.captain_num = current_captain_num
        current_try.captain_name = current_game.player_set.all()[current_captain_num].player_name
        current_game.captain_before = current_captain_num  # update captain_before
        # TODO: Do I need to save()?
        current_try.save()
        current_game.save()
    captain_name = current_try.captain_name
    is_captain = captain_name == player_name
    # current_task.final_team = current_try.team_member
    context = {'is_captain': is_captain, 'captain_name': captain_name,
               'game_id': game_id, 'task_num': task_num, 'try_num': try_num,
               'players': current_game.player_set.all(), 'team_selected': current_try.tryteammember_set.all(),
               'player_name': player_name, 'team_size': current_game.team_size[task_num-1]}
    return render(request, 'Avalon/team_makeup.html', context)


def update_team_info(request, game_id, task_num, try_num, player_name, team_size):
    current_game = AvalonGame.objects.get(game_id=game_id)
    current_task = current_game.task_set.all()[task_num - 1]
    current_try = current_task.tryteam_set.all()[try_num - 1]
    checkbox_results = [request.POST.get('team_member'+str(i), '') for i in range(1, 6)]
    checkbox_results = [checkbox_result for checkbox_result in checkbox_results if checkbox_result != '']
    for i in range(0, team_size):
        current_try.tryteammember_set.create(player_name=checkbox_results[i])
    return HttpResponseRedirect(reverse('team_makeup', args=(game_id, task_num, try_num, player_name)))


def team_makeup_vote(request, game_id, task_num, try_num, player_name):
    current_game = AvalonGame.objects.get(game_id=game_id)
    current_task = current_game.task_set.all()[task_num - 1]
    current_try = current_task.tryteam_set.all()[try_num - 1]
    if request.POST['team_makeup_vote'] == 'True':
        current_try.tryteamsupporter_set.create(player_name=player_name)
        current_try.supporter_num = current_try.supporter_num + 1
    else:
        current_try.tryteamobjector_set.create(player_name=player_name)
        current_try.objector_num = current_try.objector_num + 1
    # TODO: Do I need to save()?
    current_try.save()
    return HttpResponseRedirect(reverse('waiting_team_vote', args=[game_id, task_num, try_num, player_name]))


def waiting_team_vote(request, game_id, task_num, try_num, player_name):
    current_game = AvalonGame.objects.get(game_id=game_id)
    current_task = current_game.task_set.all()[task_num - 1]
    current_try = current_task.tryteam_set.all()[try_num - 1]
    voted_player = current_try.objector_num + current_try.supporter_num
    if voted_player == 5:
        #  make up the final team in this function
        # may not need "final team"
        # if current_try.supporter_num >= 3:
        #     if len(current_task.finalteam_set.all()) == 0:
        #         final_team = current_task.finalteam_set.create(captain_name=current_try.captain_name)
        #         for try_team_member in current_try.tryteammember_set.all():
        #             final_team.finalteammember_set.create(player_name=try_team_member.player_name)
        context = {'team_members': current_try.tryteammember_set.all(),
                   'supporters': current_try.tryteamsupporter_set.all(),
                   'objectors': current_try.tryteamobjector_set.all(),
                   'supporter_num':current_try.supporter_num,
                   'captain_name': current_try.captain_name,
                   'game_id': game_id, 'task_num': task_num, 'try_num': try_num+1, 'player_name': player_name}
        return render(request, 'Avalon/team_make_results.html', context=context)
    else:
        return render(request, 'Avalon/wait_team_vote.html')


def vote_for_task(request, game_id, task_num, player_name):
    current_game = AvalonGame.objects.get(game_id=game_id)
    current_task = current_game.task_set.all()[task_num - 1]
    tried_times = current_task.tryteam_set.count()
    final_team = [player.player_name
                  for player in current_task.tryteam_set.all()[tried_times-1].tryteammember_set.all()]
    if player_name in final_team:
        Morgana_player = get_character_player(game_id, 'Morgana')
        Assassin_player = get_character_player(game_id, 'Assassin')
        is_wicked = Morgana_player == player_name or Assassin_player == player_name
        context = {'game_id': game_id, 'task_num': task_num, 'player_name': player_name, 'is_wicked': is_wicked}
        return render(request, 'Avalon/task_voting.html', context=context)
    else:
        # return render(request, 'Avalon/wait_task_vote.html')
        return HttpResponseRedirect(reverse('waiting_task_vote', args=[game_id, task_num, player_name]))


def task_vote(request, game_id, task_num, player_name):
    current_game = AvalonGame.objects.get(game_id=game_id)
    current_task = current_game.task_set.all()[task_num - 1]
    if request.POST['task_vote'] == 'True':
        current_task.success_num = current_task.success_num + 1
    else:
        current_task.fail_num = current_task.fail_num + 1
    # TODO: Do I need to save()?
    current_task.save()
    return HttpResponseRedirect(reverse('waiting_task_vote', args=[game_id, task_num, player_name]))


def waiting_task_vote(request, game_id, task_num, player_name):
    current_game = AvalonGame.objects.get(game_id=game_id)
    current_task = current_game.task_set.all()[task_num - 1]
    tried_times = current_task.tryteam_set.count()
    final_team = [player.player_name
                  for player in current_task.tryteam_set.all()[tried_times-1].tryteammember_set.all()]
    assert current_game.team_size[task_num-1] == len(final_team)
    if current_task.success_num + current_task.fail_num < len(final_team):
        return render(request, 'Avalon/wait_task_vote.html')
    else:
        if current_game.fail_tasks_num + current_game.success_tasks_num < task_num:
            # current task result has not been recorded
            if current_task.fail_num != 0:
                current_game.fail_tasks_num = current_game.fail_tasks_num + 1
            else:
                current_game.success_tasks_num = current_game.success_tasks_num + 1
        # TODO: Do I need to save()?
        current_game.save()
        context = {'team_members': final_team,
                   'supporters_num': current_task.success_num, 'objectors_num': current_task.fail_num,
                   'game_id': game_id, 'task_num': task_num + 1, 'try_num': 1, 'player_name': player_name,
                   'finished_tasks_num': current_game.success_tasks_num,
                   'failed_tasks_num': current_game.fail_tasks_num}
        return render(request, 'Avalon/task_results.html', context=context)


def assassinate_vote(request, game_id, player_name):
    Merlin_player = get_character_player(game_id, 'Merlin')
    Assassin_player = get_character_player(game_id, 'Assassin')
    current_game = AvalonGame.objects.get(game_id=game_id)
    if player_name == Assassin_player:
        context = {'game_id': game_id, 'players': current_game.player_set.all()}
        return render(request, 'Avalon/assassin_vote.html', context=context)
    else:
        if current_game.Assassin_success is False and current_game.Assassin_fail is False:
            return render(request, 'Avalon/wait_assassinate.html')
        else:
            return render(request, 'Avalon/game_results.html',
                          context={'assassin_success': current_game.Assassin_success})


def assassinate_results(request, game_id):
    current_game = AvalonGame.objects.get(game_id=game_id)
    Merlin_player = get_character_player(game_id, 'Merlin')
    if request.POST['assassinate_choice'] == Merlin_player:
        current_game.Assassin_success = True
    else:
        current_game.Assassin_fail = True
    # TODO: Do I need to save()?
    current_game.save()
    return render(request, 'Avalon/game_results.html', context={'assassin_success': current_game.Assassin_success})
