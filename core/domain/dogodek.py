from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto


class TipDogodka(str, Enum):
	INSTRUKCIJE = auto()


@dataclass
class Dogodek:
	ime: str
	tip: TipDogodka
	zacetek: datetime
	konec: datetime
