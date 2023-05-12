import json
import os
import re
from datetime import date, datetime, timedelta

import requests

from core.domain.dogodek import Dogodek, TipDogodka
from core.domain.uporabnik import Uporabnik
from core.service.koledar_service import KoledarService


class KoledarGoogle(KoledarService):

	def __init__(self, google_api_key: str):
		self.google_api_key = google_api_key

	def dogodki(self, zacetek: date, konec: date) -> list[Dogodek]:
		api_key = os.environ.get('GOOGLE_API_KEY')
		email_naslov = os.environ.get('EMAIL')
		zacetek_ti = datetime.combine(zacetek, datetime.min.time()).isoformat() + 'Z'
		konec_ti = (datetime.combine(konec, datetime.max.time()) - timedelta(microseconds=1)).isoformat() + 'Z'
		url = f'https://www.googleapis.com/calendar/v3/calendars/{email_naslov}/events?key={api_key}&timeMin={zacetek_ti}&timeMax={konec_ti}'
		dogodki = []
		try:
			response = requests.get(url)
			response.raise_for_status()  # Error če je request.status kode čez 300
			data = json.loads(response.text)
			for event in data['items']:
				if 'description' in event:
					string = event['description']
					parsed_data = self._parsaj_string(string=string)
					uporabnik = Uporabnik(
						ime=parsed_data['name'],
						priimek=parsed_data['name'],
						email=parsed_data['email'],
						email_racuna=parsed_data['email_info'],
						telefon=parsed_data['phone']
					)
					dogodek = Dogodek(
						ime=None,
						cena=10.0,
						tip=TipDogodka.INSTRUKCIJE,
						zacetek=datetime.fromisoformat(event['start']['dateTime']),
						konec=datetime.fromisoformat(event['end']['dateTime']),
						uporabnik=uporabnik,
						placnik=parsed_data['email_info'],
						placano=False
					)
					dogodki.append(dogodek)
				else:
					print('no description, continue to next google event')
					continue
		except requests.exceptions.HTTPError as e:
			print(f"An HTTP error occurred: {e}")
		except Exception as e:
			print(f"An error occurred: {e}")
		return dogodki

	def _parsaj_string(self, string: str) -> dict:
		name = ''
		phone = ''
		email = ''
		email_info = ''

		match = re.search(r"Email osebe, ki bo plačala inštrukcije\s*:\s*([^\s<]+)", string)
		if match:
			email_info = match.group(1)
		else:
			print("Email osebe, ki bo plačala inštrukcije not found in string")

		email_match = re.search(r"Email: <a>(.+?)</a>", string)
		if email_match:
			email = email_match.group(1)

		name_match = re.search(r"Name: (.+?)<br>", string)
		if name_match:
			name = name_match.group(1)

		phone_match = re.search(r"Phone: (.+?)<br>", string)
		if phone_match:
			phone = phone_match.group(1)

		return {'name': name, 'phone': phone, 'email': email, 'email_info': email_info}
