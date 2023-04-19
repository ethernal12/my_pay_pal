from dataclasses import dataclass


@dataclass
# informacija o ucencu
class Uporabnik:
	ime: str
	priimek: str
	email: str
	telefon: str
	email_racuna: str  # email kamor bo poslan racun


