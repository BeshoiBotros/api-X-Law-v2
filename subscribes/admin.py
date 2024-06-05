from django.contrib import admin
from . import models

admin.site.register(models.Subscribe)
admin.site.register(models.SubscribeContract)
admin.site.register(models.SubscribeOrder)
admin.site.register(models.Limit)
