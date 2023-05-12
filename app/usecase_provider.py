from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import DependenciesContainer, Factory, Provider

from app.service_provider import ServiceProvider
from core.use_cases.ustvari_racunsko_porocilo import Ustvari_racunsko_porocilo


class UseCaseProvider(DeclarativeContainer):
	d: ServiceProvider = DependenciesContainer()

	ustvari_racunsko_porocilo: Provider[Ustvari_racunsko_porocilo] = Factory(
		Ustvari_racunsko_porocilo,
		_knjiga_racunov=d.knjiga_racunov,
		_koledar=d.koledar
	)
