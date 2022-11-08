from django.urls import path
from UserApp.api import views as api_views


urlpatterns = [
    path('DiscordAcc/<int:pk>', api_views.UyeAccListCreateAPIView.as_view(), name="yazarlarListesi"),
]