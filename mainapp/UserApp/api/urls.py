from django.urls import path
from UserApp.api import views as api_views


urlpatterns = [
    path('DiscordAcc/<int:pk>', api_views.UyeAccListCreateAPIView.as_view(), name="DiscordLog"),
    path('User/<int:pk>', api_views.UyeAPIView.as_view(), name="uye"),
]