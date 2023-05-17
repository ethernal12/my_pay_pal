from datetime import date, datetime, timezone

import stripe

from core.domain.denar import DenarnaVrednost, Valute
from core.domain.porocilo import KnjizniVnos
from core.domain.uporabnik import Uporabnik
from core.service.knjiga_racunov_service import KnjigaRacunovService


class KnjigaRacunovStripe(KnjigaRacunovService):

	def __init__(self, stripe_api_key: str):
		stripe.api_key = stripe_api_key

	def knjizni_vnosi(self, zacetek: date, konec: date) -> list[KnjizniVnos]:
		knjizenja = []

		zacetek_dt = datetime(zacetek.year, zacetek.month, zacetek.day, tzinfo=timezone.utc)
		konec_dt = datetime(konec.year, konec.month, konec.day, 23, 59, 59)
		invoices = stripe.Invoice.list(created={"gte": int(zacetek_dt.timestamp()), "lt": int(konec_dt.timestamp())})

		for invoice in invoices:
			customer = stripe.Customer.retrieve(invoice.customer)
			uporabnik = Uporabnik(
				ime=customer.name,
				priimek=customer.name,
				email=None,
				email_racuna=customer.email,
				telefon=customer.phone
			)
			# pretvori iz usd v euro že pri vseh dobljenih invojsih
			if invoice.currency == 'usd':
				cena = DenarnaVrednost(vrednost=invoice.amount_due / 100.0, valuta=Valute.dolar)
				cena = cena.pretvori(valuta=Valute.euro)
			else:
				cena = DenarnaVrednost(vrednost=invoice.amount_due / 100.0, valuta=Valute.euro)
				datum = datetime.fromtimestamp(invoice['lines']['data'][0]['price'].created)
			knjizni_vnos = KnjizniVnos(
				placnik=uporabnik,
				cena=cena,
				datum=datum,
				namen=invoice['lines']['data'][0]['description'],
				placano=invoice.paid
			)
			knjizenja.append(knjizni_vnos)
		return knjizenja
