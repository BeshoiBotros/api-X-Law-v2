from django.contrib import admin
from . import models

admin.site.register(models.New)
admin.site.register(models.SolvedCase)
admin.site.register(models.Category)