# MY_PAYPAL APP

## Namen aplikacije:
### Aplikacija vrne vse dogodke iz google koledarja in vse stripe invoice v poljubnem koledarskem obdobju in naredi primerjavo med njimi. Uporabniku sporoči kateri google dogodki se ujemajo z stripe invoici, na podlagi e-maila.

## Uporaba apklikacije:
### Uporabnik prvo izbere datume na koledarju v obsegu od - do in pritisne gumb Ustvari poročilo, ta vrne vse google dogodke v tem časovnem obdobju in vse stripe invoice, ki so bili poslani v tem obdobju. Ko so naloženi vsi google dogodki in stripe invoici v obe tabele, lahko uporabnik pritisne gumb MatchTables, ki začne z primerjavo obeh tabel.
Tabele se po pritisku te tipke tudi obarvajo, za vsak e-mail naslov je dodeljena posebna barva, tako da če je v tabelah ni obarvana katerakoli vrstica je napaka ujemanja kvanitete.
Uporabniku tudi nato sporoči kaj se ne ujema in koliko., če se vsi stripe invoici ujemajo z google eventi, je poslano sporočilo "Vsi email naslovi imajo pravilne kvantitete med tabelami.".

## Inštalacija aplikacije:
### Po kloniranju REPO se inštalirajo vse potrebne knjižnice z ukazom v terminalu pip install -r requirements.txt in aplikacija se lahko zažene z vstopom v folder app in ukazom v terminalu py GUI.py.
