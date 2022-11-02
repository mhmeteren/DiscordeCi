from django.urls import path
from . import views
urlpatterns = [
    path('firma/', views.login, name='login'),
    path('firma/index/', views.index, name='index'),
    path('firma/logout/', views.logout, name='logout'),
]