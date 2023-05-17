from dataclasses import dataclass
from datetime import date, timedelta
from typing import Optional
from core.domain.denar import DenarnaVrednost, Valuta, Valute
from core.domain.dogodek import Dogodek
from core.domain.uporabnik import Uporabnik


@dataclass
class KnjizniVnos:
	placnik: Uporabnik
	cena: DenarnaVrednost
	datum: date
	namen: str
	placano:bool

@dataclass
class ElementRacuna:
	dogodek: Dogodek
	knjizni_vnos: Optional[KnjizniVnos]


@dataclass
class DnevnoRacunskoPorocilo:
	datum: date
	elementi: list[ElementRacuna]

	def cena_dogodkov(self, valuta: Valuta = Valute.euro) -> DenarnaVrednost:
		dv = DenarnaVrednost(vrednost=0, valuta=valuta)
		for e in self.elementi:
			dv.pristej(e.knjizni_vnos.cena)
		return dv


@dataclass
class RacunskoPorocilo:
	zacetek: date
	konec: date
	dnevi: list[DnevnoRacunskoPorocilo]

	@property
	def dolzina(self) -> timedelta:
		return self.konec - self.zacetek
