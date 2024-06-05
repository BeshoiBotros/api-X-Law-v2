from django.contrib import admin
from . import models
from django.contrib.contenttypes.models import ContentType

admin.site.register(models.CustomUser)
admin.site.register(models.Client)
admin.site.register(models.Lawyer)
admin.site.register(models.VerifyToken)
admin.site.register(models.LawyerProfile)
admin.site.register(ContentType)