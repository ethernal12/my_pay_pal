from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Provider, Singleton

from app import ENV
from app.service.knjiga_racunov_stripe import KnjigaRacunovStripe
from app.service.koledar_google import KoledarGoogle


class ServiceProvider(DeclarativeContainer):
	knjiga_racunov: Provider[KnjigaRacunovStripe] = Singleton(KnjigaRacunovStripe, stripe_api_key=ENV.STRIPE_API_KEY)
	koledar: Provider[KoledarGoogle] = Singleton(KoledarGoogle, google_api_key=ENV.GOOGLE_API_KEY)