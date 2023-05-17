import datetime
import unittest

from dependency_injector.providers import Provider

from app import APP, ENV
from app.service.knjiga_racunov_stripe import KnjigaRacunovStripe
from core.use_cases.ustvari_racunsko_porocilo import Ustvari_racunsko_porocilo


class MyFactory:
	def __init__(self, class_ref, *args, **kwargs):
		self.class_ref = class_ref
		self.args = args
		self.kwargs = kwargs
		print("INIT")

	def __call__(self, *args, **kwargs):
		print("CALL")
		return self.class_ref(*self.args, **self.kwargs)

ustvari_racunsko_porocilo: Provider[Ustvari_racunsko_porocilo] = MyFactory(
	Ustvari_racunsko_porocilo, _knjiga_racunov=KnjigaRacunovStripe(stripe_api_key=ENV.STRIPE_API_KEY))

urp = ustvari_racunsko_porocilo()

print(urp)

#
# class Test_instrukcije(unittest.TestCase):
# 	@classmethod
# 	def setUpClass(cls) -> None:
# 		APP.init()
# 		cls.use_case = APP.use_case.ustvari_racunsko_porocilo()
#
# 	def test_dogodki(self):
# 		today = datetime.date.today()
# 		rp = self.use_case.exe(zacetek=today, konec=today + datetime.timedelta(days=2))
# 		assert len(rp.dnevi) > 0