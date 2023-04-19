from abc import ABC, abstractmethod
from datetime import date

from core.domain.dogodek import Dogodek


class KoledarService(ABC):
	@abstractmethod
	def dogodki(self, zacetek: date, konec: date) -> list[Dogodek]:
		pass
