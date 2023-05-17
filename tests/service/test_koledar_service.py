import datetime
import unittest

from app import APP


class Test_knjiga_racunov_service(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		APP.init()
		cls.service = APP.services.koledar()


	def test_dogodki(self):
		today = datetime.date.today()
		dogodki = self.service.knjizni_vnosi(zacetek=today, konec=today + datetime.timedelta(days=2))
		assert len(dogodki) > 0