from django.urls import path

from . import views


urlpatterns = [
    path('webhook/', views.UpdatesHandlerBotAPIView.as_view(), name='update')
]
