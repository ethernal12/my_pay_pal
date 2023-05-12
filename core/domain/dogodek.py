from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum, auto

from core.domain.uporabnik import Uporabnik


class TipDogodka(str, Enum):
	INSTRUKCIJE = auto()


@dataclass
class Dogodek:
	ime: str
	cena: float
	tip: TipDogodka
	zacetek: datetime
	konec: datetime
	uporabnik: Uporabnik
	placnik: Uporabnik
	placano: bool

	@property
	def dolzina(self) -> timedelta:
		return self.konec - self.zacetek
