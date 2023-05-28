import logging
from collections import defaultdict

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTableWidgetItem, QLabel, QMessageBox, QPushButton

log = logging.getLogger(__name__)


class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(1037, 900)

		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")

		# Nastavi začetne datume
		default_start_date = QtCore.QDate(2023, 5, 2)
		default_end_date = QtCore.QDate(2023, 5, 9)

		self.exit_button = QPushButton("Izhod", self.centralwidget)
		self.exit_button.setGeometry(900, 800, 75, 30)
		self.exit_button.clicked.connect(MainWindow.close)

		self.start_date_edit = QtWidgets.QDateEdit(self.centralwidget)
		self.start_date_edit.setGeometry(QtCore.QRect(150, 50, 150, 30))
		self.start_date_edit.setCalendarPopup(True)
		self.start_date_edit.dateChanged.connect(self.update_start_date)

		self.end_date_edit = QtWidgets.QDateEdit(self.centralwidget)
		self.end_date_edit.setGeometry(QtCore.QRect(150, 100, 150, 30))
		self.end_date_edit.setCalendarPopup(True)
		self.end_date_edit.dateChanged.connect(self.update_end_date)

		self.start_date_edit.setDate(default_start_date)
		self.end_date_edit.setDate(default_end_date)

		self.match_events_btn = QtWidgets.QPushButton(MainWindow)
		self.match_events_btn.setGeometry(QtCore.QRect(420, 750, 171, 51))
		self.match_events_btn.setText("matchTables")
		self.match_events_btn.clicked.connect(
			lambda: self.barvno_poudari_email(self.stripe_tabela.currentRow()))

		self.generiraj_poročila_btn = QtWidgets.QPushButton(self.centralwidget)
		self.generiraj_poročila_btn.setGeometry(QtCore.QRect(420, 70, 171, 51))

		self.generiraj_poročila_btn.setObjectName("generirajPorocila")
		self.generiraj_poročila_btn.clicked.connect(self.populiraj_tabele)
		self.stripe_tabela = QtWidgets.QTableWidget(self.centralwidget)
		self.stripe_tabela.setGeometry(QtCore.QRect(150, 170, 321, 520))
		# stripe tabela
		self.stripe_tabela.setObjectName("stripeInvoiceTable")
		self.stripe_tabela.setColumnCount(0)
		self.stripe_tabela.setRowCount(0)
		self.google_tabela = QtWidgets.QTableWidget(self.centralwidget)
		self.google_tabela.setGeometry(QtCore.QRect(530, 170, 321, 520))

		# google events tabela
		self.google_tabela.setObjectName("googleEventsTable")
		self.google_tabela.setColumnCount(0)
		self.google_tabela.setRowCount(0)
		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 1037, 26))
		self.menubar.setObjectName("menubar")
		self.menuStripe_google_calendar_porocilo = QtWidgets.QMenu(self.menubar)
		self.menuStripe_google_calendar_porocilo.setObjectName("stripe & google_poročilo")
		MainWindow.setMenuBar(self.menubar)
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)
		self.menubar.addAction(self.menuStripe_google_calendar_porocilo.menuAction())

		label_datumi = QLabel("Izberi datume:", self.centralwidget)
		label_datumi.setGeometry(150, 20, 321, 30)

		label_od = QLabel("Od:", self.centralwidget)
		label_od.setGeometry(50, 50, 50, 30)

		label_do = QLabel("Do:", self.centralwidget)
		label_do.setGeometry(50, 100, 50, 30)

		label_stripe = QLabel("STRIPE-POROČILO", self.centralwidget)
		label_stripe.setAlignment(Qt.AlignCenter)

		font = QFont()
		font.setBold(True)
		label_stripe.setFont(font)

		label_stripe.setGeometry(150, 140, 321, 30)

		label_google = QLabel("GOOGLE-POROČILO", self.centralwidget)
		label_google.setAlignment(Qt.AlignCenter)

		label_google.setFont(font)

		label_google.setGeometry(530, 140, 321, 30)
		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def update_start_date(self, date):
		self.start_date = date.toPyDate()

	def update_end_date(self, date):
		self.end_date = date.toPyDate()

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
		self.generiraj_poročila_btn.setText(_translate("MainWindow", "Ustvari poročilo"))
		self.menuStripe_google_calendar_porocilo.setTitle(_translate("MainWindow", "Stripe & google calendar porocilo"))

	def populiraj_tabele(self):

		APP.init()
		service = APP.use_case.ustvari_racunsko_porocilo()
		zacetek = self.start_date
		konec = self.end_date
		rp = service.exe(zacetek=zacetek, konec=konec)

		self.stripe_tabela.clearContents()

		self.google_tabela.setRowCount(len(rp.dnevi))
		column_labels = ["Začetek", "Konec", "Naslov inštrukcije", "Ime", "Email", "Email računa", "Telefonska", "Cena"]
		self.google_tabela.setColumnCount(len(column_labels))
		self.google_tabela.setHorizontalHeaderLabels(column_labels)

		column_labels = ["Ime", "Email učenca", "Čas knjiženja", "Račun", "Cena"]

		self.stripe_tabela.setColumnCount(len(column_labels))
		self.stripe_tabela.setHorizontalHeaderLabels(column_labels)

		invoices_by_day = defaultdict(list)
		events_by_day = defaultdict(list)

		for dnevno_rp in rp.dnevi:
			for element in dnevno_rp.elementi:
				if element.knjizni_vnos:
					invoice_date = element.knjizni_vnos.datum.date()
					invoices_by_day[invoice_date].append(element)
				elif element.dogodek:
					event_date = element.dogodek.zacetek.date()
					events_by_day[event_date].append(element)

			sorted_days = sorted(events_by_day.keys())

			self.google_tabela.setRowCount(sum(len(events_by_day[day]) for day in sorted_days))
			row = 0

			for event_date in sorted_days:
				events = events_by_day[event_date]
				prvi_event = True

				for event in events:
					# pretvori iz dolarja v evre
					valuta_ime = event.dogodek.cena.valuta.ime
					cena = event.dogodek.cena.vrednost
					simbol_valute = "$" if valuta_ime == "dollar" else "€"
					cena_with_symbol = simbol_valute + str(cena)

					zacetek_item = QTableWidgetItem(str(event.dogodek.zacetek))
					konec_item = QTableWidgetItem(str(event.dogodek.konec))
					naslov_item = QTableWidgetItem(event.dogodek.ime)
					ime_item = QTableWidgetItem(event.dogodek.uporabnik.ime)
					email_item = QTableWidgetItem(event.dogodek.uporabnik.email)
					email_racuna_item = QTableWidgetItem(event.dogodek.uporabnik.email_racuna)
					telefon_item = QTableWidgetItem(event.dogodek.uporabnik.telefon)
					cena_item = QTableWidgetItem(cena_with_symbol)

					# če je prvi event prikaži samo datum
					if prvi_event:
						date_str = event.dogodek.zacetek.date().strftime("%Y-%m-%d")
						self.google_tabela.setVerticalHeaderItem(row, QTableWidgetItem(date_str))
						prvi_event = False
					else:
						# če imamo več dogodkov na isti dan nastavi row header na prazno
						self.google_tabela.setVerticalHeaderItem(row, QTableWidgetItem(""))

					self.google_tabela.setItem(row, 0, zacetek_item)
					self.google_tabela.setItem(row, 1, konec_item)
					self.google_tabela.setItem(row, 2, naslov_item)
					self.google_tabela.setItem(row, 3, ime_item)
					self.google_tabela.setItem(row, 4, email_item)
					self.google_tabela.setItem(row, 5, email_racuna_item)
					self.google_tabela.setItem(row, 6, telefon_item)
					self.google_tabela.setItem(row, 7, cena_item)

					row += 1

		sorted_days = sorted(invoices_by_day.keys())

		self.stripe_tabela.setRowCount(sum(len(invoices_by_day[day]) for day in sorted_days))
		row = 0

		for invoice_date in sorted_days:
			invoices = invoices_by_day[invoice_date]
			date_str = invoice_date.strftime("%Y-%m-%d")

			date_item = QTableWidgetItem(date_str)
			self.stripe_tabela.setVerticalHeaderItem(row, date_item)

			for i, invoice in enumerate(invoices):
				if invoice.knjizni_vnos:
					name = invoice.knjizni_vnos.placnik.ime
					email = invoice.knjizni_vnos.placnik.email_racuna
					date = invoice.knjizni_vnos.datum
					date_str = date.strftime("%Y-%m-%d %H:%M:%S")
					racun_placan = "plačano" if invoice.knjizni_vnos.placano else "ni plačano"
					cena = invoice.knjizni_vnos.cena.vrednost
					valuta_ime = invoice.knjizni_vnos.cena.valuta.ime

					simbol_valute = "$" if valuta_ime == "dollar" else "€"
					cena_with_symbol = simbol_valute + str(cena)
					name_item = QTableWidgetItem(name)
					email_item = QTableWidgetItem(email)
					date_item = QTableWidgetItem(date_str)
					racun_item = QTableWidgetItem(racun_placan)
					cena_item = QTableWidgetItem(str(cena_with_symbol))
					# če je prvi invoice, napiši samo datum
					if i == 0:
						date_item = QTableWidgetItem(date_str)
						self.stripe_tabela.setVerticalHeaderItem(row, date_item)
					else:

						hour = date.strftime("%H:%M:%S")
						hour_item = QTableWidgetItem(
							"                    " + hour)
						self.stripe_tabela.setVerticalHeaderItem(row, hour_item)
					self.stripe_tabela.setItem(row, 0, name_item)
					self.stripe_tabela.setItem(row, 1, email_item)
					self.stripe_tabela.setItem(row, 2, date_item)
					self.stripe_tabela.setItem(row, 3, racun_item)
					self.stripe_tabela.setItem(row, 4, cena_item)

				row += 1

		self.stripe_tabela.resizeColumnsToContents()
		self.stripe_tabela.resizeRowsToContents()

		self.google_tabela.resizeColumnsToContents()
		self.google_tabela.resizeRowsToContents()

	def barvno_poudari_email(self, selected_row):
		stripe_table = self.stripe_tabela
		google_table = self.google_tabela
		# vsakič resetiraj barvo tabele na belo
		for row in range(google_table.rowCount()):
			for row in range(google_table.columnCount()):
				item = google_table.item(row, row)
				if item is not None:
					item.setBackground(Qt.white)

		for row in range(stripe_table.rowCount()):
			for row in range(stripe_table.columnCount()):
				item = stripe_table.item(row, row)
				if item is not None:
					item.setBackground(Qt.white)

		unique_google_email = []
		all_google_emails = []
		all_stripe_emails = []

		for google_row in range(google_table.rowCount()):
			google_email_item = google_table.item(google_row, 4)
			google_email = google_email_item.text()
			all_google_emails.append(google_email)

			if google_email not in unique_google_email:
				unique_google_email.append(google_email)
		# generiraj unikatno barvo za vsak unikaten email naslov
		email_colors = self.generiraj_random_barve(len(unique_google_email))

		for google_row in range(google_table.rowCount()):
			google_email_item = google_table.item(google_row, 4)
			google_email = google_email_item.text()

			for email, color in zip(unique_google_email, email_colors):
				if google_email == email:

					for column in range(google_table.columnCount()):
						google_table.item(google_row, column).setBackground(color)

		for stripe_row in range(stripe_table.rowCount()):
			stripe_email_item = stripe_table.item(stripe_row, 1)
			stripe_email = stripe_email_item.text()
			all_stripe_emails.append(stripe_email)

			for email, color in zip(unique_google_email, email_colors):
				if stripe_email == email:

					for column in range(stripe_table.columnCount()):
						item = stripe_table.item(stripe_row, column)
						if item is not None:
							item.setBackground(color)
		self.primerjaj_tabele(all_google_emails, all_stripe_emails)

	def primerjaj_tabele(self, google_emails, stripe_emails):
		google_counts = {}
		stripe_counts = {}

		for email in google_emails:
			google_counts[email] = google_counts.get(email, 0) + 1

		for email in stripe_emails:
			stripe_counts[email] = stripe_counts.get(email, 0) + 1

		mismatched_emails = []
		for email, google_count in google_counts.items():
			stripe_count = stripe_counts.get(email, 0)
			if google_count != stripe_count:
				mismatched_emails.append((email, google_count, stripe_count))

		missing_emails = [email for email in stripe_counts if email not in google_counts]

		if mismatched_emails or missing_emails:
			message = "Naslednji email noslovi imajo razliko v kvantiteti med tabelama:\n\n"
			for email, google_count, stripe_count in mismatched_emails:
				message += f"{email} - Google: {google_count}, Stripe: {stripe_count}\n"
			for email in missing_emails:
				message += f"{email} - Google: 0, Stripe: {stripe_counts[email]}\n"
		else:
			message = "Vsi email naslovi imajo pravilne kvantitete med tabelami."

		msg_box = QMessageBox()
		msg_box.setWindowTitle("Razlika v kvantiteti email naslovov")
		msg_box.setText(message)
		msg_box.setIcon(QMessageBox.Warning)
		msg_box.exec_()

	def generiraj_random_barve(self, num_colors):
		colors = []
		hue_step = 360.0 / num_colors

		for i in range(num_colors):
			hue = i * hue_step
			color = QColor.fromHsvF(hue / 360.0, 1.0, 1.0)
			colors.append(color)

		return colors


if __name__ == "__main__":
	import sys

	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())
