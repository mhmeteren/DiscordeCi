from rest_framework import serializers
from UserApp.models import Uye, UyeDiscordLog


from datetime import datetime
from django.utils.timesince import timesince


class UyeDiscordLogSerializer(serializers.ModelSerializer):


    class Meta:
        model = UyeDiscordLog
        fields = '__all__'
        read_only_fields = ['UyeID', 'DiscordID', 'TOKEN', 'UyeDiscordLogTARIH']
    

  