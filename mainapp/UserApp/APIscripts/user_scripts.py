import requests

from FirmaApp.models import *

def getFirmaAPIurls(API, FirmaID):
    try:
        api = apiaccess.objects.get(FirmaID = FirmaID, API=API)
        return api.APIUrl
    except:
        return None

def UserTokenAut(FirmaID, token):
    url = f'{getFirmaAPIurls(apiaccessChoices.UserAuth, FirmaID)}/{token}/'
    r = requests.get(url)
    if r.status_code == 200:
        return r.content
    return None