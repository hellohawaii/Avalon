from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from Avalon.models import AvalonGame
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
    # print(game.remained_characters)
    random_character = random.choice(game.remained_characters)
    game.assigned_characters.append(random_character)
    game.remained_characters.remove(random_character)
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
    intro['Merlin'] = 'You knows who are wicked people, %s and %s is wicked' % (Morgana_player, Assassin_player)
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
    current_task = current_game.tasks[task_num-1]
    current_try = current_task.team_trys[try_num-1]
    # use index of player to represent the captain
    if not current_try.captain:
        # choose a captain when the first user want to make up a team
        current_captain = (current_game.captain_before + 1) % 5
        current_try.captain = current_captain
        current_game.captain_before = current_captain  # update captain_before
    else:
        pass
    captain_name = current_game.player_set.all()[current_try.captain].player_name
    is_captain = captain_name == player_name

    context = {'is_captain': is_captain, 'game_id': game_id, 'task_num': task_num, 'try_num': try_num,
               'players': current_game.player_set.all(), 'team_selected': current_try.team_member,
               'player_name': player_name, 'team_size': current_game.team_size[task_num-1]}
    return render(request, 'Avalon/team_makeup.html', context)


def update_team_info(request, game_id, task_num, try_num, player_name, team_size):
    current_game = AvalonGame.objects.get(game_id=game_id)
    current_task = current_game.tasks[task_num - 1]
    current_try = current_task.team_trys[try_num - 1]
    checkbox_results = [request.POST.get('team_member'+str(i), '') for i in range(1, 6)]
    checkbox_results = [checkbox_result for checkbox_result in checkbox_results if checkbox_result != '']
    current_try.team_member = checkbox_results[0:team_size]
    # print(current_try.team_member)
    return HttpResponseRedirect(reverse('team_makeup', args=(game_id, task_num, try_num, player_name)))


def team_makeup_vote(request, game_id, task_num, try_num, player_name):
    current_game = AvalonGame.objects.get(game_id=game_id)
    current_task = current_game.tasks[task_num - 1]
    current_try = current_task.team_trys[try_num - 1]
    if request.POST['team_makeup_vote'] == 'True':
        current_try.supporters.append(player_name)
        current_try.supporter_num = current_try.supporter_num + 1
    else:
        current_try.objectors.append(player_name)
        current_try.objector_num = current_try.objector_num + 1
    return HttpResponseRedirect(reverse('waiting_team_vote', args=[game_id, task_num, try_num]))


def waiting_team_vote(request,game_id, task_num, try_num):
    current_game = AvalonGame.objects.get(game_id=game_id)
    current_task = current_game.tasks[task_num - 1]
    current_try = current_task.team_trys[try_num - 1]
    voted_player = current_try.objector_num + current_try.supporter_num
    if voted_player == 5:
        context = {'current_try': current_try}
        return render(request, 'Avalon/team_make_results.html', context=context)
    else:
        return render(request, 'Avalon/wait_team_vote.html')

