import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from autologging import traced
from app import ENV
from app.service_provider import ServiceProvider
from app.usecase_provider import UseCaseProvider
from core import cutils

this = sys.modules[__name__]
this.use_case: UseCaseProvider
this.services: ServiceProvider

log = logging.getLogger(__name__)
logging.basicConfig(
	level=ENV.LOG_LEVEL,
	format="%(asctime)s.%(msecs)03d ┃ %(filename)+20s:%(lineno)d ┃ %(funcName)-30s ┃ %(levelname)+8s ┃ %(message)s",
	datefmt="%Y-%m-%d %H:%M:%S",
	handlers=[
		TimedRotatingFileHandler(
			when='midnight',
			interval=1,
			encoding='utf-8',
			filename=cutils.root_path("logging.log")
		),
		logging.StreamHandler()
	]
)


def init():
	this.services = ServiceProvider()
	this.use_case = UseCaseProvider(d=this.services)
