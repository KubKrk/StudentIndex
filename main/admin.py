from django.contrib import admin
from .models import CustomUser, Group

admin.site.register(CustomUser)
admin.site.register(Group)

