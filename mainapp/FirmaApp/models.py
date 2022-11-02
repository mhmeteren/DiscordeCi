from xml.etree.ElementInclude import default_loader
from django.db import models


class Firma(models.Model):

    FirmaID = models.AutoField(primary_key=True)
    FirmaADI = models.CharField(max_length=50)
    FirmaBILGI = models.CharField(max_length=200)
    FirmaEMAIL = models.CharField(max_length=50)
    FirmaSIFRE = models.CharField(max_length=128)
    FirmaDURUM = models.BooleanField(default=False)
    FirmaRESIMURL = models.URLField(max_length=200)
    FirmaTARIH = models.DateTimeField(auto_now_add=True)
    FirmaYONETICI = models.CharField(max_length=100)

    class Meta:
        db_table = "Firma"
    
    def __str__(self):
        return self.FirmaADI
 
    def auth(self):
        firma = Firma.objects.filter(FirmaEMAIL=self.FirmaEMAIL, FirmaSIFRE=self.FirmaSIFRE).first()
        return firma


#--------------------------------------------------------------------------------------------------------------------------------


class Discord(models.Model):
    DiscordID = models.AutoField(primary_key=True)
    FirmaID = models.BigIntegerField() #models.ForeignKey(Firma, on_delete=models.CASCADE)
    DiscordANLIKUYE = models.BigIntegerField()
    DiscordMAXUYE = models.BigIntegerField()
    DiscordANLIKSATIS = models.BigIntegerField()
    DiscordTOPSATIS = models.BigIntegerField()
    DiscordTOPCALISAN = models.BigIntegerField()
    DiscordANLIKCALISAN = models.BigIntegerField()
    DiscordSupport = models.BigIntegerField()
    class Meta:
        db_table = "Discord"    

    def get_Discord_Status(self):
        return Discord.objects.get(FirmaID=self.FirmaID)
        


#--------------------------------------------------------------------------------------------------------------------------------
