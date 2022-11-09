from django.shortcuts import render, redirect
from django.db.models import Q
from django.views.decorators.http import require_http_methods


from hashlib import sha256
from secrets import token_hex
from .models import Uye, UyeAcc,Firma, UyeDiscordLog, UyeAdres,  WalletLogStatus, UyeWalletLog
from decimal import Decimal


def getHASH(password):
    return sha256(password.encode('utf-8')).hexdigest()


def login(request):
    if request.session.get('UyeID') is not None:
        return redirect("user_index")
        
    if request.method == 'POST':
        passwd = getHASH(request.POST["password"])
        user = Uye(UyeUSERNAME=request.POST["acc"],  UyePASSWORD=passwd, UyeEMAIL=request.POST["acc"])
        user = Uye.auth(user)
        

        if not user:
            return render(request, 'signin.html', {
            'error': 'email, username veya password yanlış!!'
            })
        
        else:
            request.session.modified = True
            refreshAcc(request, user.UyeID)            
            
            return redirect("user_index")

    return render(request, 'login.html')


def logout(request):
    request.session.flush()
    return redirect('user_login')

def refreshAcc(request, UserID: int):
    user = Uye.objects.filter(UyeID=UserID).first()

    if user:
        request.session["UyeID"] =  user.UyeID
        request.session["DiscordID"] =  user.DiscordID
        request.session["UyeUSERNAME"] =  user.UyeUSERNAME
        request.session["UyeEMAIL"] =  user.UyeEMAIL
        request.session["UyeWALLET"] =  str(user.UyeWALLET)
        request.session["UyeDURUM"] =  int(user.UyeDURUM)
   
  
@require_http_methods(["GET"]) 
def index(request):
   
    try:
        UserID = int(request.session.get('UyeID'))
    except TypeError:
        return redirect('user_login')
        
    return _Return_index(request, UserID)

"""
index sayfasının GET motodu ve 
Token ekledikten sonra yönlendirme  için
"""
def _Return_index(request, UserID):
    acc = UyeAcc(UyeID=Uye(UyeID=UserID))
    acclist = acc.get_All_Firma()
    

    refreshAcc(request, UserID)
    WalletDate = UyeWalletLog.objects.filter(UyeID = Uye(UyeID = UserID), UyeWalletLogIslem = WalletLogStatus.YUKLEME).last()

    content = { 
        'session': request.session,
        'acclist': acclist,
        'WalletDate': WalletDate
    }

    return render(request, 'UserHome.html', context=content)

def allAccounts(request, userid= None, firmaid= None, isacc= None):
    try:
        UserID = int(request.session.get('UyeID'))
    except TypeError:
        return redirect('user_login')
    UyeAcc.objects.filter(UyeID=Uye(UyeID=userid), FirmaID=Firma(FirmaID=firmaid)).update(UyeAccDURUM=bool(isacc))
    return redirect("user_index")

     
def signup(request):
    if request.session.get('UyeID') is not None:
        return redirect("user_index")
    
    if request.method == 'POST':
        
        if Uye.objects.filter(UyeUSERNAME=request.POST["username"]).first() is not None:
            return render(request, 'signup.html', {
            'error': 'Bu username kullanilamaz!!'
            })

        if Uye.objects.filter(UyeEMAIL=request.POST["email"]).first() is not None:
            return render(request, 'signup.html', {
            'error': 'Bu email adresi kullanilamaz!!'
            })
        
        
        
       
        uye = Uye(UyeUSERNAME = request.POST["username"],
        UyePASSWORD = getHASH(request.POST["password"]),
        UyeEMAIL = request.POST["email"])
        uye.save()
        return render(request, 'signup.html', {
            'succ': 'Kayıt islemi basarili'
            })

    return render(request, 'signup.html')

def getAllFirma():
    return Firma.objects.filter(FirmaDURUM=True)
     

@require_http_methods(["GET"]) 
def settings(request):
    
    try:
        UserID = int(request.session.get('UyeID'))
    except TypeError:
        return redirect('user_login')

    refreshAcc(request, UserID)
    adresList = getAdresList(UserID)

    dcAut = UyeDiscordLog.objects.filter(UyeID = Uye(UyeID=UserID), TOKENDURUM=False).first()

    WalletDate = UyeWalletLog.objects.filter(UyeID = Uye(UyeID = UserID), UyeWalletLogIslem = WalletLogStatus.YUKLEME).last()
    WalletLog = getWalletLog(UserID)
    FirmaList = getAllFirma()
    content = { 
        'session': request.session,
        'adresList': adresList,
        'WalletDate': WalletDate,
        'WalletLog': WalletLog,
        'FirmaList': FirmaList,
        'dcAut': dcAut
    }
    return render(request, 'settings.html', context=content)

@require_http_methods(["POST"])  
def AccUpdate(request):
    try:
        UserID = int(request.session.get('UyeID'))
    except TypeError:
        return redirect('user_login')

    if Uye.objects.filter(UyeID=UserID, UyePASSWORD=getHASH(request.POST["mypassword"])).first() is None:
        return render(request, 'settings.html', {
            'session': request.session,
            'Accerror': 'Girilen parola yanlış'
        })
     
    email = str(request.POST["email"]).replace(' ','')
    if (request.session.get('UyeEMAIL') != email) and Uye.objects.filter(UyeEMAIL=email):
        return render(request, 'settings.html', {
            'session': request.session,
            'Accerror': 'Girilen email kullanılamaz!!'
         
        })
    
    username = str(request.POST["username"]).replace(' ','')
    if (request.session.get('UyeUSERNAME') != username) and Uye.objects.filter(UyeUSERNAME=username):
        return render(request, 'settings.html', {
            'session': request.session,
            'Accerror': 'Girilen Username kullanılamaz!!'
        })
    durum = True if request.POST.get('dc', bool(request.session.get('UyeDURUM'))) == 'on' else False
    Uye.objects.filter(UyeID=int(request.session.get('UyeID'))).update(UyeUSERNAME=request.POST["username"],
    UyeEMAIL=request.POST["email"], UyeDURUM=durum)
    refreshAcc(request, int(request.session.get('UyeID')))
    content = { 
    'session': request.session,
    'Accsuccess': 'işlem başarılı'
    }
    return render(request, 'settings.html', context=content)

@require_http_methods(["POST"])  
def PassUpdate(request):
    try:
        UserID = int(request.session.get('UyeID'))
    except TypeError:
        return redirect('user_login')
    
    
    if Uye.objects.filter(UyeID=UserID, UyePASSWORD=getHASH(request.POST["mypassword"])).first() is None:
        return render(request, 'settings.html', {
            'session': request.session,
            'errorPassword': 'Girilen parola yanlış!',
        })
    if request.POST["newpasswordagain"] != request.POST["newpassword"]:
        return render(request, 'settings.html', {
            'session': request.session,
            'errorPassword': 'Girilen yeni parolalar aynı olmalıdır!',
        })
    if request.POST["mypassword"] == request.POST["newpassword"]:
        return render(request, 'settings.html', {
            'session': request.session,
            'errorPassword': 'Yeni parola ile eski parola aynı olamaz!!',
        })
    
    Uye.objects.filter(UyeID=UserID).update(UyePASSWORD=getHASH(request.POST["newpassword"]))
    return render(request, 'settings.html', {
                'session': request.session,
                'successPassword': 'Parolanız başarılı bir şekilde güncellendi',
            })
  
@require_http_methods(["POST"])  
def DcUpdate(request):
    try:
        userID = int(request.session.get('UyeID'))
    except TypeError:
        return redirect('user_login')

    
    
    if Uye.objects.filter(UyeID=userID, UyePASSWORD=getHASH(request.POST["mypassword"])).first() is None:
        return render(request, 'settings.html', {
            'session': request.session,
            'errorDiscordid':'Girilen parola yanlış',
        })

    dc_log = UyeDiscordLog.objects.filter(UyeID = Uye(UyeID=userID), TOKENDURUM=False).first()
    if  dc_log:
        return render(request, 'settings.html', {
            'session': request.session,
            'errorDiscordid':'Aktif edilmemiş Discord Hesabınız mevcut!!',
            'answer': '!activate '+ dc_log.TOKEN
        })

    if request.session.get('DiscordID') != str(request.POST["mydiscordid"]).replace(' ',''):
        return render(request, 'settings.html', {
            'session': request.session,
            'errorDiscordid':'Girilen Discord ID yanlış',
        })


    DiscordID = str(request.POST["newdiscordid"]).replace(' ','')
    if len(DiscordID) != 19 or DcidControl(DiscordID, userID):
        return render(request, 'settings.html', {
            'session': request.session,
            'errorDiscordid':'Girilen yeni Discord ID yanlış',
        })

        
    return UyeDiscordLog_Save(request, DiscordID, userID)
        
        
@require_http_methods(["POST"])  
def DcSave(request):
    try:
        userID = int(request.session.get('UyeID'))
    except TypeError:
        return redirect('user_login')

    refreshAcc(request, userID)
    dc = str(request.POST["newdiscordid"]).replace(' ','')

    if Uye.objects.filter(UyeID=userID, UyePASSWORD=getHASH(request.POST["mypassword"])).first() is None:
        return render(request, 'settings.html', {
            'session': request.session,
            'passwd': 'Girilen parola yanlış'
           
            })

    if len(dc) != 19 or DcidControl(dc, userID):
        return render(request, 'settings.html', {
            'session': request.session,
            'passwd': 'Girilen Discord id  yanlış veya kullanılamaz!!'
           
            })
    
    if  UyeDiscordLog.objects.filter(UyeID = Uye(UyeID=userID), TOKENDURUM=False).first():
        return render(request, 'settings.html', {
            'session': request.session,
            'passwd': 'Aktif edilmemiş Discord Hesabınız mevcut!!'
           
            })

    return UyeDiscordLog_Save(request, dc, userID)

def UyeDiscordLog_Save(request, DiscordID, userID):
    Token = token_hex(9)
    discord = UyeDiscordLog(UyeID=Uye(UyeID=userID), DiscordID=DiscordID, TOKEN=Token)
    discord.save()
    refreshAcc(request, userID)
    return render(request, 'settings.html', {
                'session': request.session,
                'passwdsucc':'Discord ID kaydedildi, hesabınızı onaylamak için Discord sunucumuzda size özel kanalda ilgili cevabı 5 dk içinde girin. Aksi taktirde işlem iptal edilir',
                'answer': '!activate '+ Token
            })


def DcidControl(DiscordID, userID):
    dc_user = Uye.objects.filter(DiscordID=DiscordID).first()
    dc_log = UyeDiscordLog.objects.filter(~Q(UyeID=Uye(UyeID=userID)) ,DiscordID=DiscordID, TOKENDURUM=False).first()
    return (dc_log is not None or dc_user is not None)


def getAdresList(UserID):
    return UyeAdres.objects.filter(UyeID=(Uye(UyeID=UserID)))

@require_http_methods(["POST"])     
def AdresSave(request):
    try:
        userID = int(request.session.get('UyeID'))
    except TypeError:
        return redirect('user_login')
    
    adres = UyeAdres(UyeID=(Uye(UyeID=userID)), UyeAdresBASLIK=request.POST["baslik"][:50],
    UyeAdresALICI=request.POST["alici"][:50], UyeAdres=request.POST["adres"][:300],
    UyeAdresALICIGSM=request.POST["gsm"][:11], UyeAdresALICITC=request.POST["tc"][:11])
    adres.save()
    adresList = getAdresList(userID)
    
    return render(request, 'settings.html', {
                'session': request.session,
                'adresList': adresList,
                'Adres': 'Adres başarılı bir şekilde kaydedildi'
            })

@require_http_methods(["GET"])       
def AdresDelete(request, adresid):
    try:
        userID = int(request.session.get('UyeID'))
    except TypeError:
        return redirect('user_login')
    
    if UyeAdres.objects.filter(UyeID=(Uye(UyeID=userID)), UyeAdresID=adresid) is not None:
        UyeAdres.objects.filter(UyeAdresID=adresid).delete()

    adresList = getAdresList(userID)
    return render(request, 'settings.html', {
                'session': request.session,
                'adresList': adresList
            })


def AdresUpdate(request, adresid):
    try:
        userID = int(request.session.get('UyeID'))
    except TypeError:
        return redirect('user_login')

    if request.method == 'POST':
        if UyeAdres.objects.filter(UyeID=(Uye(UyeID=userID)), UyeAdresID=adresid) is not None:

            UyeAdres.objects.filter(UyeID=(Uye(UyeID=userID)), UyeAdresID=adresid).update(
            UyeAdresBASLIK=request.POST["baslik"][:50],
            UyeAdresALICI=request.POST["alici"][:50], UyeAdres=request.POST["adres"][:300],
            UyeAdresALICIGSM=request.POST["gsm"][:11], UyeAdresALICITC=request.POST["tc"][:11])

        adresList = getAdresList(userID)
        return render(request, 'settings.html', {
                    'session': request.session,
                    'adresList': adresList
                })


        

    if UyeAdres.objects.filter(UyeID=(Uye(UyeID=userID)), UyeAdresID=adresid) is not None:
        adres = UyeAdres.objects.filter(UyeID=(Uye(UyeID=userID)), UyeAdresID=adresid).first()
        adresList = getAdresList(userID)
        return render(request, 'settings.html', {
                    'session': request.session,
                    'adresList': adresList,
                    'adresUpdate': adres
                })

@require_http_methods(["POST"])
def CheckOut(request):
    try:
        userID = int(request.session.get('UyeID'))
    except TypeError:
        return redirect('user_login')
    
  
    amount = Decimal(request.POST["amount"])
    wallet = Uye.objects.get(UyeID = userID).UyeWALLET
    walletLog = UyeWalletLog(UyeID = Uye(UyeID=userID), UyeWALLET = wallet, UyeWalletLogIslem = WalletLogStatus.YUKLEME,
    UyeWalletLogAmount = amount)
    walletLog.save()
    
    Uye.objects.filter(UyeID = userID).update(UyeWALLET=(wallet+amount))
    WalletDate = UyeWalletLog.objects.filter(UyeID = Uye(UyeID = userID), UyeWalletLogIslem = WalletLogStatus.YUKLEME).last()
    WalletLog = getWalletLog(userID)
    
    refreshAcc(request, userID)
    return render(request, 'settings.html', {
                    'session': request.session,
                    'WalletDate': WalletDate,
                    'WalletLog': WalletLog
                })
        

def getWalletLog(userID):
    return UyeWalletLog.objects.filter(UyeID = Uye(UyeID = userID)).reverse()[:5]
    
@require_http_methods(["POST"])
def addToken(request):
    try:
        userID = int(request.session.get('UyeID'))
    except TypeError:
        return redirect('user_login')
    
    FirmaList = getAllFirma()
    if Uye.objects.filter(UyeID=userID, UyePASSWORD=getHASH(request.POST["mypassword"])).first() is None:
        return render(request, 'settings.html', {
            'session': request.session,
            'addTokenError':'Girilen parola yanlış',
            'FirmaList': FirmaList
        })
    
    token = request.POST["token"][:128]
    """ Unique TOKEN"""
    if UyeAcc.objects.filter(UyeAccTOKEN=token).first() is not None:
        return render(request, 'settings.html', {
            'session': request.session,
            'addTokenError':'Girilen TOKEN eksik veya hattalı!!',
            'FirmaList': FirmaList
        })

    """Bir firmaya sadece bir token eklenebilir"""
    firma = Firma(FirmaID = int(request.POST["firma"])) 
    UyeAcc.objects.filter(UyeID = Uye(UyeID = userID), FirmaID = firma).delete()

    uyeacc = UyeAcc(UyeID = Uye(UyeID = userID), FirmaID = firma,
    UyeAccTOKEN = token)

    uyeacc.save()
    return _Return_index(request, userID)
