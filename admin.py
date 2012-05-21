from django.contrib import admin
from footballscores.models import *

admin.site.register(Competition)
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Fixture)
admin.site.register(Goal)

