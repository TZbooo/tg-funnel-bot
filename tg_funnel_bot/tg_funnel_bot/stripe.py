import stripe
from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_API_KEY