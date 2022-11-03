from django.shortcuts import render, redirect
from FirmaApp.models import Firma, Discord
from hashlib import sha256

def login(request):
    if request.session.get('ID') is not None:
        return redirect('firma_index')

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
            return redirect("firma_index")

    return render(request, 'signin.html')

def logout(request):
    request.session.flush()
    return redirect('firma_login')

def index(request):
    if request.session.get('ID') is None:
        return redirect('firma_login')

    discord = Discord(FirmaID=Firma(FirmaID=request.session.get("ID")))
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