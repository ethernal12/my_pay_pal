import datetime
import unittest

from app import APP


class Test_ustvari_racunsko_porocilo(unittest.TestCase):
	@classmethod
	def setUpClass(cls) -> None:
		APP.init()
		cls.use_case = APP.use_case.ustvari_racunsko_porocilo()

	def test_dogodki(self):
		today = datetime.date.today()
		rp = self.use_case.exe(zacetek=today, konec=today + datetime.timedelta(days=2))
		assert len(rp.dnevi) > 0