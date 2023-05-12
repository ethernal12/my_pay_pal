from datetime import date

from app import APP
from core.domain.porocilo import RacunskoPorocilo


class GUI:
	def dobi_invoice(self) -> RacunskoPorocilo:
		APP.init()
		service = APP.use_case.ustvari_racunsko_porocilo()
		zacetek = date(2023, 5, 1)
		konec = date(2023, 5, 4)
		rp = service.exe(zacetek=zacetek, konec=konec)
		return rp


gui = GUI()
rp_result = gui.dobi_invoice()
print(f'---------------računsko poročilo OD: {rp_result.zacetek} DO: {rp_result.konec}---------------------')
for dnevno_rp in rp_result.dnevi:
	print(f'----------------------------datum: {dnevno_rp.datum}------------------')
	for element in dnevno_rp.elementi:
		if element.dogodek:
			print('------------------nov dogodek----------------------')
			print(f"Zacetek: {element.dogodek.zacetek}")
			print(f"Konec: {element.dogodek.konec}")
			print(f"Naslov inšt.: {element.dogodek.ime}")
			print('Uporabnik')
			print(f"\tIme: {element.dogodek.uporabnik.ime}")
			print(f"\tEmail: {element.dogodek.uporabnik.email}")
			print(f"\tEmail racuna: {element.dogodek.uporabnik.email_racuna}")
			print(f"\tTelefonska: {element.dogodek.uporabnik.telefon}")
		else:
			print('Ni drugega dogodka!')
		if element.knjizni_vnos:
			print('----------------------knjizenje-----------------------')
			print(
				f'knjizni_vnos_cena : {element.knjizni_vnos.cena.vrednost} valuta: {element.knjizni_vnos.cena.valuta.ime}')
			print('knjizni_vnos_placnik:')
			print(f"\tIme: {element.knjizni_vnos.placnik.ime}")
			print(f"\tPriimek: {element.knjizni_vnos.placnik.priimek}")
			print(f"\tČas knjiženja:: {element.knjizni_vnos.datum}")
			# če je učenec podal email za pošiljanje računa, drugače uporabi email učenca samega
			email = element.knjizni_vnos.placnik.email_racuna if element.knjizni_vnos.placnik.email_racuna is not None else element.knjizni_vnos.placnik.email
			print(f"\tRačun poslan na email: {email}")
			print(f"\tTelefon: {element.knjizni_vnos.placnik.telefon}")
			print(f'Racun : {"je plačan" if element.knjizni_vnos.placano else "ni plačan"}')
		else:
			print('Ni drugega knjiženja!')
