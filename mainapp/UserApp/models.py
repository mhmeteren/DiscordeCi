from django.db import models
from django.db.models import Q
from hashlib import sha256
from FirmaApp.models import Firma

class Uye(models.Model):

    UyeID = models.AutoField(primary_key=True)
    DiscordID = models.CharField(max_length=25, null=True, unique=True, editable=True)
    UyeUSERNAME = models.CharField(max_length=15, unique=True)
    UyePASSWORD = models.CharField(max_length=128)
    UyeEMAIL = models.EmailField(max_length=50, unique=True)
    UyeWALLET = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    UyeDURUM = models.BooleanField(default=False)

    class Meta:
        db_table = "Uye"
        verbose_name= "Uye"
        verbose_name_plural = "Uyeler"
    
    def __str__(self):
        return self.UyeUSERNAME
 
    def auth(self):
        user = Uye.objects.filter(Q(UyeUSERNAME=self.UyeUSERNAME) | Q(UyeEMAIL=self.UyeEMAIL),
        UyePASSWORD=self.UyePASSWORD).first()
        return user

    def save(self):
        self.UyePASSWORD = sha256(self.UyePASSWORD.encode('utf-8')).hexdigest()
        super(Uye, self).save()
#----------------------------------------------------------------------------------------------------------------------------------

class UyeAcc(models.Model):

    UyeAccID = models.AutoField(primary_key=True)
    UyeID = models.ForeignKey(Uye, on_delete=models.CASCADE, name = "UyeID")
    FirmaID = models.ForeignKey(Firma, on_delete=models.CASCADE, name = "FirmaID")
    UyeAccTOKEN = models.CharField(max_length=128)
    UyeAccDURUM = models.BooleanField(default=False)
    UyeAccTARIH = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "UyeAcc"

    def get_All_Firma(self):
        AccList = UyeAcc.objects.filter(UyeID = self.UyeID.UyeID)
        return AccList

    def __str__(self):
        return self.UyeID
#-----------------------------------------------------------------------------------------------------------------------------------

class UyeAdres(models.Model):

    UyeAdresID = models.AutoField(primary_key=True)
    UyeID = models.ForeignKey(Uye, on_delete=models.CASCADE, name = "UyeID")
    UyeAdresBASLIK = models.CharField(max_length=50)
    UyeAdresALICI = models.CharField(max_length=50)
    UyeAdres = models.CharField(max_length=300)
    UyeAdresALICIGSM = models.CharField(max_length=11)
    UyeAdresALICITC = models.CharField(max_length=11)

    class Meta:
        db_table = "UyeAdres"

    def __str__(self):
        return self.UyeID
#-----------------------------------------------------------------------------------------------------------------------------------

class WalletLogStatus(models.TextChoices):
    YUKLEME = 'YUKLEME', 'Yükleme'
    ALISVERIS = 'ALISVERIS', 'AlisVeris'

    

class UyeWalletLog(models.Model):

    UyeWalletLogID = models.AutoField(primary_key=True)
    UyeID = models.ForeignKey(Uye, on_delete=models.CASCADE, name = "UyeID")
    UyeWALLET = models.DecimalField(max_digits=15, decimal_places=2)
    UyeWalletLogIslem = models.CharField(max_length=50, choices=WalletLogStatus.choices)
    UyeWalletLogAmount = models.DecimalField(max_digits=15, decimal_places=2)
    UyeWalletLogTARIH = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "UyeWalletLog"

    def __str__(self):
        return self.UyeID
#-----------------------------------------------------------------------------------------------------------------------------------

class UyeDiscordLog(models.Model):

    UyeDiscordLogID = models.AutoField(primary_key=True)
    UyeID = models.ForeignKey(Uye, on_delete=models.CASCADE, name = "UyeID")
    DiscordID = models.CharField(max_length=25, unique=True, editable=True)
    TOKEN = models.CharField(max_length=18, editable=True)
    TOKENDURUM = models.BooleanField(default=False)
    UyeDiscordLogTARIH = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "UyeDiscordLog"

    def __str__(self):
        return self.UyeID
#-----------------------------------------------------------------------------------------------------------------------------------

class UyeAccisDead(models.Model):
    DeadID = models.AutoField(primary_key=True)
    DiscordID = models.CharField(max_length=25, editable=True)
    FirmaID = models.ForeignKey(Firma, on_delete=models.CASCADE, name = "FirmaID")
    DeadDate = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "UyeAccisDead"

    def __str__(self):
        return f'{self.FirmaID} - {self.DiscordID}'
#-----------------------------------------------------------------------------------------------------------------------------------