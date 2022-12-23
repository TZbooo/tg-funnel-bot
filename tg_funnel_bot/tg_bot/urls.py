from django.urls import path

from . import views


urlpatterns = [
    path('telegram-webhooks/', views.TelegramUpdatesAPIView.as_view(), name='telegram-updates'),
    path('stripe-updates/', views.StripeUpdatesAPIView.as_view(), name='stripe-updates'),
]
