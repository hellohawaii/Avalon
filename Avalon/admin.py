from django.contrib import admin
# Register your models here.

from .models import AvalonGame, Player, Task, \
    TryTeam, TryTeamMember, \
    TryTeamSupporter, TryTeamObjector, AssignedCharacter, RemainedCharacter
# from .models import FinalTeam, FinalTeamMember

admin.site.register(AvalonGame)
admin.site.register(Player)
admin.site.register(Task)
admin.site.register(TryTeam)
admin.site.register(TryTeamMember)
# admin.site.register(FinalTeam)
# admin.site.register(FinalTeamMember)
admin.site.register(TryTeamSupporter)
admin.site.register(TryTeamObjector)
admin.site.register(AssignedCharacter)
admin.site.register(RemainedCharacter)
