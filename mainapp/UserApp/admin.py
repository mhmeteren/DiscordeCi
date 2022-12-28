from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    #fields = ('UyeUSERNAME', 'UyeEMAIL')
    readonly_fields = ('DiscordID', 'UyeWALLET',)

admin.site.register(Uye, UserAdmin)
admin.site.register(UyeAcc)
admin.site.register(UyeAdres)
admin.site.register(UyeWalletLog)
admin.site.register(UyeDiscordLog)
admin.site.register(UyeAccisDead)
admin.site.register(UyeAlisverisLog)