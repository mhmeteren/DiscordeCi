from rest_framework import serializers
from UserApp.models import Uye, UyeDiscordLog, UyeAccisDead



class UyeDiscordLogSerializer(serializers.ModelSerializer):


    class Meta:
        model = UyeDiscordLog
        fields = '__all__'
        read_only_fields = ['UyeID', 'DiscordID', 'TOKEN', 'UyeDiscordLogTARIH']


class UyeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Uye
        fields = ['UyeID', 'DiscordID', 'UyeUSERNAME']
        read_only_fields = ['UyeID' ,'UyeUSERNAME']


class UyeAccisDeadSerializer(serializers.ModelSerializer):

    class Meta:
        model = UyeAccisDead
        fields = '__all__'
        read_only_fields = ['DeadID', 'DeadDate']