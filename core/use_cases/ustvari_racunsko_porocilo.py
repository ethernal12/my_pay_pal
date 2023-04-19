from datetime import date, timedelta

from core.domain.porocilo import RacunskoPorocilo, DnevnoRacunskoPorocilo
from core.service.knjiga_racunov_service import KnjigaRacunovService
from core.service.koledar_service import KoledarService
from core.use_cases._use_case import Use_case


class Ustvari_racunsko_porocilo(Use_case):
	koledar: KoledarService
	knjiga_racunov: KnjigaRacunovService

	def exe(self, zacetek: date, konec: date) -> RacunskoPorocilo:
		rp = RacunskoPorocilo(zacetek=zacetek, konec=konec, dnevi=[])
		rp.dolzina.days
		dogodkov = self.koledar.dogodki(zacetek=zacetek, konec=konec)
		for i in range(rp.dolzina.days):
			dd = zacetek + timedelta(days=i)
			drr = DnevnoRacunskoPorocilo(datum=dd, elementi=[])
			rp.dnevi.append(drr)
