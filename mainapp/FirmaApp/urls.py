from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.login, name='firma_login'),
    path('index/', views.index, name='firma_index'),
    path('logout/', views.logout, name='firma_logout'),
]