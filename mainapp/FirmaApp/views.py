from django.shortcuts import render, redirect
from FirmaApp.models import Firma, Discord
from hashlib import sha256

def login(request):

    if request.method == 'POST':
        passwd = sha256(request.POST["password"].encode('utf-8')).hexdigest()
        firma = Firma(FirmaEMAIL=request.POST["email"],  FirmaSIFRE=passwd)
        firm = Firma.auth(firma)
        

        if not firm:
            return render(request, 'signin.html', {
            'error': 'email veya password yanlış!!'
            })
        
        else:
            request.session["ID"] =  firm.FirmaID
            request.session["ADI"] =  firm.FirmaADI
            request.session["YONETICI"] =  firm.FirmaYONETICI
            return redirect("index")

    return render(request, 'signin.html')

def logout(request):
    request.session.flush()
    return redirect('login')

def index(request):
    discord = Discord(FirmaID=request.session.get("ID"))
    dis = discord.get_Discord_Status()
    content = { 
        'session':request.session,
        'id': request.session.get("ID"),
        'adi': request.session.get("ADI"),
        'yonetici':request.session.get("YONETICI"),
        'discord': dis,
    }
    return render(request, 'index.html', context=content)
"""
def DiscordSetings(request):
    content = { 
        'session':request.session,
        'id': request.session.get("ID"),
        'adi': request.session.get("ADI"),
        'yonetici':request.session.get("YONETICI"),
    
    }
    return render(request, 'setings.html', context=content)
"""