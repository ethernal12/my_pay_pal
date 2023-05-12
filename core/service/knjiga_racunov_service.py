from abc import ABC, abstractmethod
from datetime import date

from core.domain.porocilo import KnjizniVnos


class KnjigaRacunovService(ABC):
	@abstractmethod
	def knjizni_vnosi(self, zacetek: date, konec: date) -> list[KnjizniVnos]:
		pass


