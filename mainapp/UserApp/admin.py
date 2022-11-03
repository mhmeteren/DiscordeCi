from django.contrib import admin
from .models import Uye


class UserAdmin(admin.ModelAdmin):
    #fields = ('UyeUSERNAME', 'UyeEMAIL')
    readonly_fields = ('DiscordID', 'UyeWALLET',)

admin.site.register(Uye, UserAdmin)
