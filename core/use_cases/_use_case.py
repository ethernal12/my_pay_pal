from abc import ABC, abstractmethod


class Use_case(ABC):
	@abstractmethod
	def exe(self, *args, **kwargs):
		pass



