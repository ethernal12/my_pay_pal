import sys
from app import ENV
from app.service_provider import ServiceProvider
from app.usecase_provider import UseCaseProvider

this = sys.modules[__name__]
this.use_case: UseCaseProvider
this.services: ServiceProvider


def init():
	this.services = ServiceProvider()
	this.use_case = UseCaseProvider(d=this.services)