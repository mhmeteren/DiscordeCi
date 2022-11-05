from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.login, name='user_login'),
    path('index/', views.index, name='user_index'),
    path('logout/', views.logout, name='user_logout'),
    path('account/<int:userid>/<int:firmaid>/<int:isacc>/', views.allAccounts, name='user_account'),
    path('signup/', views.signup, name='user_signup'),
    path('settings/', views.settings, name='user_settings'),
    path('accupdate/', views.AccUpdate, name='user_accupdate'),
    path('passupdate/', views.PassUpdate, name='user_passupdate'),
    path('dcupdate/', views.DcUpdate, name='user_dcupdate'),
    path('dcsave/', views.DcSave, name='user_dcsave'),
    path('adressave/', views.AdresSave, name='user_adressave'),
    path('adresdel/<int:adresid>/', views.AdresDelete, name='user_adresdel'),
    path('adresup/<int:adresid>/', views.AdresUpdate, name='user_adresup'),
    path('checkout/', views.CheckOut, name='user_checkout'),
]