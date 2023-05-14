from dataclasses import dataclass
from datetime import date, timedelta
from core.domain.porocilo import RacunskoPorocilo, DnevnoRacunskoPorocilo, ElementRacuna, KnjizniVnos
from core.service.knjiga_racunov_service import KnjigaRacunovService
from core.service.koledar_service import KoledarService
from core.use_cases._use_case import Use_case


@dataclass
class Ustvari_racunsko_porocilo(Use_case):
	_knjiga_racunov: KnjigaRacunovService
	_koledar: KoledarService

	def exe(self, zacetek: date, konec: date) -> RacunskoPorocilo:
		knjizni_vnosi = self._knjiga_racunov.knjizni_vnosi(zacetek=zacetek, konec=konec)
		google_dogodki = self._koledar.dogodki(zacetek=zacetek, konec=konec)
		rp = RacunskoPorocilo(zacetek=zacetek, konec=konec, dnevi=[])
		for i in range(rp.dolzina.days + 1):
			elementi = []
			dd = zacetek + timedelta(days=i)
			for dogodek in google_dogodki:
				if dogodek.zacetek.date() == dd:
					element = ElementRacuna(
						dogodek=dogodek,
						knjizni_vnos=None
					)
					elementi.append(element)
			for knjizni_vnos in knjizni_vnosi:
				if knjizni_vnos.datum.date() == dd:
					element = ElementRacuna(
						dogodek=None,
						knjizni_vnos=knjizni_vnos
					)
					elementi.append(element)

			drr = DnevnoRacunskoPorocilo(datum=dd, elementi=elementi)
			rp.dnevi.append(drr)
		return rp
