from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.login, name='user_login'),
    path('index/', views.index, name='user_index'),
    path('logout/', views.logout, name='user_logout'),
    path('account/<int:userid>/<int:firmaid>/<int:isacc>/', views.account, name='user_account'),
    path('signup/', views.signup, name='user_signup'),
    path('settings/', views.settings, name='user_settings'),
]