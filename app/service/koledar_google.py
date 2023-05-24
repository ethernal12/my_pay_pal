import json
import logging
import re
import traceback
from datetime import date, datetime, timedelta

import requests

from core.domain.denar import DenarnaVrednost, Valute
from core.domain.dogodek import Dogodek, TipDogodka
from core.domain.uporabnik import Uporabnik
from core.service.koledar_service import KoledarService

log = logging.getLogger(__name__)


class InformacijeEventa:
	def __init__(self, name: str, phone: str, email: str, email_placnik: str, cena_instrukcij: float, cena_valuta: str):
		self.name = name
		self.phone = phone
		self.email = email
		self.email_placnik = email_placnik
		self.cena_instrukcij = cena_instrukcij
		self.cena_valuta = cena_valuta


class KoledarGoogle(KoledarService):

	def __init__(self, google_api_key: str, google_email_naslov: str):
		self.google_api_key = google_api_key
		self.email_naslov = google_email_naslov

	def dogodki(self, zacetek: date, konec: date) -> list[Dogodek]:
		zacetek_ti = datetime.combine(zacetek, datetime.min.time()).isoformat() + 'Z'
		konec_ti = (datetime.combine(konec, datetime.max.time()) - timedelta(microseconds=1)).isoformat() + 'Z'
		url = f'https://www.googleapis.com/calendar/v3/calendars/{self.email_naslov}/events?key={self.google_api_key}&timeMin={zacetek_ti}&timeMax={konec_ti}'
		dogodki = []
		try:
			response = requests.get(url)
			# Error če je request.status kode čez 300
			response.raise_for_status()
			data = json.loads(response.text)
			for event in data['items']:
				if 'description' in event:
					string = event['description']
					acuity_id_pattern = re.compile(r"AcuityID=(\d+)")
					match = acuity_id_pattern.search(string)
					if match:
						dobljene_informacije_dogodka = self._dobi_informacije_dogodka(string=string)
						if dobljene_informacije_dogodka.cena_valuta == '$':
							cena = DenarnaVrednost(vrednost=dobljene_informacije_dogodka.cena_instrukcij,
							                       valuta=Valute.dolar)
							cena = cena.pretvori(valuta=Valute.euro)
						else:

							cena = DenarnaVrednost(vrednost=dobljene_informacije_dogodka.cena_instrukcij,
							                       valuta=Valute.euro)
						uporabnik = Uporabnik(
							ime=dobljene_informacije_dogodka.name,
							priimek=dobljene_informacije_dogodka.name,
							email=dobljene_informacije_dogodka.email,
							email_racuna=dobljene_informacije_dogodka.email_placnik,
							telefon=dobljene_informacije_dogodka.phone
						)
						dogodek = Dogodek(
							ime=None,
							cena=cena,
							tip=TipDogodka.INSTRUKCIJE,
							zacetek=datetime.fromisoformat(event['start']['dateTime']),
							konec=datetime.fromisoformat(event['end']['dateTime']),
							uporabnik=uporabnik
						)
						dogodki.append(dogodek)
					else:

						log.info("AcuityID ni najden na tem dogodku")
				else:
					log.info('ni opisa na dogodku, nadaljuj na naslednji dogodek')
					continue
		except requests.exceptions.HTTPError as e:
			log.error(f"An HTTP error occurred: {e}")
		except Exception as e:
			log.error(f"An error occurred: {e}\n{traceback.format_exc()}")
		return dogodki

	def _dobi_informacije_dogodka(self, string: str) -> InformacijeEventa:
		name = ''
		phone = ''
		email = ''
		email_placnik = ''
		cena_instrukcij = None

		email_regex = r'Email osebe, ki bo plačala inštrukcije : </span><a><u><u>(.*?)</u></u></a>'
		placnik_meil_match = re.search(email_regex, string)

		if placnik_meil_match:
			email_placnik = placnik_meil_match.group(1)
		else:
			log.info("Email osebe, ki bo plačala inštrukcije not found in string")

		email_match = re.search(r"Email: <a>(.+?)</a>", string)
		if email_match:
			email = email_match.group(1)

		name_match = re.search(r"Name: (.+?)<br>", string)
		if name_match:
			name = name_match.group(1)

		phone_match = re.search(r"Phone: (.+?)<br>", string)
		if phone_match:
			phone = phone_match.group(1)

		cena_match = re.search(r"Price: (?:\$|€)([\d.]+)", string)
		if cena_match:
			cena_instrukcij = float(cena_match.group(1))

		valuta_match = re.search(r"Price:\s*(\D+)", string)
		if valuta_match:
			cena_valuta = valuta_match.group(1)
		else:
			cena_valuta = None
		return InformacijeEventa(name=name, phone=phone, email=email, email_placnik=email_placnik,
		                         cena_instrukcij=cena_instrukcij, cena_valuta=cena_valuta)
