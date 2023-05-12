import os
from datetime import date, datetime, timezone, timedelta

import stripe

from core.domain.denar import DenarnaVrednost, Valute
from core.domain.dogodek import Dogodek, TipDogodka
from core.domain.uporabnik import Uporabnik
from core.service.knjiga_racunov_service import KnjigaRacunovService


class KnjigaRacunovStripe(KnjigaRacunovService):

	def __init__(self, stripe_api_key: str):
		stripe.api_key = stripe_api_key

	def knjizni_vnosi(self, zacetek: date, konec: date) -> list[Dogodek]:
		dogodki = []

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
			dogodek = Dogodek(
				ime=invoice.description,
				cena=cena.vrednost,
				tip=TipDogodka.INSTRUKCIJE,
				zacetek=datetime.fromtimestamp(invoice.created),
				konec=datetime.fromtimestamp(invoice.created) + timedelta(hours=1),
				uporabnik=uporabnik,
				placnik=uporabnik,
				placano=invoice.paid
			)
			dogodki.append(dogodek)
		return dogodki
