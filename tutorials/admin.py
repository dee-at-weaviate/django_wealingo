from django.contrib import admin

from .models import Questions_Inventory, User_Profile, Questions_Type

admin.site.register(Questions_Inventory)
admin.site.register(User_Profile)
admin.site.register(Questions_Type)