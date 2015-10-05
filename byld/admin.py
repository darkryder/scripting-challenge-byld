from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import *

admin.site.register(Team)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(CompetetionTimeConfiguration, SingletonModelAdmin)