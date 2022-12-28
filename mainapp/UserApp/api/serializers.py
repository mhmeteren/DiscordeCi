from rest_framework import serializers
from UserApp.models import Uye, UyeDiscordLog, UyeAccisDead, UyeAcc, UyeAdres, UyeWalletLog, UyeAlisverisLog



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


class UyeAccSerializer(serializers.ModelSerializer):

    class Meta:
        model = UyeAcc
        fields = '__all__'


class UyeAdresSerializer(serializers.ModelSerializer):

    class Meta:
        model = UyeAdres
        fields = '__all__'


class UyeDiscordControlSerializer(serializers.ModelSerializer):
    UyeAdres = UyeAdresSerializer(read_only=True, many=True)
    class Meta:
        model = Uye
        exclude = ["UyePASSWORD", "UyeDURUM"]


class UyeWalletLogserializer(serializers.ModelSerializer):
    
    class Meta:
        model = UyeWalletLog
        fields = '__all__'


class UyeAlisverisLogserializer(serializers.ModelSerializer):
    
    class Meta:
        model = UyeAlisverisLog
        fields = '__all__'