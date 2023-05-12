from dataclasses import dataclass


@dataclass
class Valuta:
	ime: str
	simbol: str
	koda: str
	exrate: float


@dataclass
class Valute:
	euro = Valuta(ime='evro', simbol='€', koda='EUR', exrate=1)
	dolar = Valuta(ime='dollar', simbol='$', koda='USD', exrate=1.1)


@dataclass
class DenarnaVrednost:
	vrednost: float
	valuta: Valuta

	def pretvori(self, valuta: Valuta) -> 'DenarnaVrednost':
		eu_vrednost = self.vrednost / self.valuta.exrate
		return DenarnaVrednost(valuta=valuta, vrednost=eu_vrednost * valuta.exrate)

	def pristej(self, dv: 'DenarnaVrednost'):
		sdv = dv.pretvori(valuta=self.valuta)
		self.vrednost += sdv.vrednost
