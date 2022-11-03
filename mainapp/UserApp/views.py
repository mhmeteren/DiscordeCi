from django.shortcuts import render, redirect
from hashlib import sha256
from .models import Uye, UyeAcc,Firma


def login(request):
    if request.session.get('UyeID') is not None:
        return redirect('user_index')
        
    if request.method == 'POST':
        passwd = sha256(request.POST["password"].encode('utf-8')).hexdigest()
        user = Uye(UyeUSERNAME=request.POST["acc"],  UyePASSWORD=passwd, UyeEMAIL=request.POST["acc"])
        user = Uye.auth(user)
        

        if not user:
            return render(request, 'signin.html', {
            'error': 'email, username veya password yanlış!!'
            })
        
        else:
            request.session["UyeID"] =  user.UyeID
            request.session["DiscordID"] =  user.DiscordID
            request.session["UyeUSERNAME"] =  user.UyeUSERNAME
            request.session["UyeEMAIL"] =  user.UyeEMAIL
            request.session["UyeWALLET"] =  str(user.UyeWALLET)
            request.session["UyeDURUM"] =  int(user.UyeDURUM)
            
            
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

  

def index(request):
    if request.session.get('UyeID') is None:
        return redirect('user_login')

    UserID = int(request.session.get('UyeID'))
    acc = UyeAcc(UyeID=Uye(UyeID=UserID))
    acclist = acc.get_All_Firma()
    refreshAcc(request, UserID)
    content = { 
        'session': request.session,
        'acclist': acclist,
    }

    return render(request, 'UserHome.html', context=content)

def account(request, userid= None, firmaid= None, isacc= None):
    if request.session.get('UyeID') is None:
        return redirect('user_login')
    UyeAcc.objects.filter(UyeID=Uye(UyeID=userid), FirmaID=Firma(FirmaID=firmaid)).update(UyeAccDURUM=bool(isacc))
    return redirect("user_index")
    
def signup(request):
    if request.session.get('UyeID') is not None:
        return redirect('user_index')
    
    if request.method == 'POST':
        """
        if Uye.objects.filter(UyeEMAIL=request.POST["email"]) is not None:
            return render(request, 'signup.html', {
            'errormail': 'Bu email adresi kullanilamaz!!'
            })
        
        if Uye.objects.filter(UyeUSERNAME=request.POST["username"]) is not None:
            return render(request, 'signup.html', {
            'errorname': 'Bu username kullanilamaz!!'
            })
        """
       
        uye = Uye(UyeUSERNAME = request.POST["username"],
        UyePASSWORD = sha256(request.POST["password"].encode('utf-8')).hexdigest(),
        UyeEMAIL = request.POST["email"])
        uye.save()
        return render(request, 'login.html', {
            'case': 'Kayıt islemi basarili'
            })

    return render(request, 'signup.html')


def settings(request):
    UserID = int(request.session.get('UyeID'))
    refreshAcc(request, UserID)
    content = { 
        'session': request.session,
    }
    print(request.session.get('UyeDURUM'))
    return render(request, 'settings.html', context=content)