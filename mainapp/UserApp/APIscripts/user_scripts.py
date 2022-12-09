import os
import sys


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

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