from django.db import models
from hashlib import sha256

class Firma(models.Model):

    FirmaID = models.AutoField(primary_key=True)
    FirmaADI = models.CharField(max_length=50)
    FirmaBILGI = models.CharField(max_length=200)
    FirmaEMAIL = models.CharField(max_length=50)
    FirmaSIFRE = models.CharField(max_length=128)
    FirmaDURUM = models.BooleanField(default=False)
    FirmaTARIH = models.DateTimeField(auto_now_add=True)
    FirmaYONETICI = models.CharField(max_length=100)

    class Meta:
        db_table = "Firma"
        verbose_name = "Firma"
        verbose_name_plural = "Firmalar"
    
    def __str__(self):
        return self.FirmaADI
 
    def auth(self):
        firma = Firma.objects.filter(FirmaEMAIL=self.FirmaEMAIL, FirmaSIFRE=self.FirmaSIFRE).first()
        return firma

    def save(self):
        self.FirmaSIFRE = sha256(self.FirmaSIFRE.encode('utf-8')).hexdigest()
        super(Firma, self).save()

#--------------------------------------------------------------------------------------------------------------------------------


class Discord(models.Model):
    DiscordID = models.AutoField(primary_key=True)
    FirmaID = models.ForeignKey(Firma, on_delete=models.CASCADE)
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

class apiaccessChoices(models.TextChoices):
    UserAuth = 'UserAuth'
    Products = 'Products'


class apiaccess(models.Model):
    apiaccessID = models.AutoField(primary_key=True)
    FirmaID = models.ForeignKey(Firma, on_delete=models.CASCADE)
    API = models.CharField(max_length=50, choices=apiaccessChoices.choices)
    APIUrl = models.URLField(max_length=200)

    class Meta:
        db_table = "apiaccess"
        
    def __str__(self):
        return f'Firma: {self.FirmaID} - API: {self.API} - APIUrl: {self.APIUrl}'