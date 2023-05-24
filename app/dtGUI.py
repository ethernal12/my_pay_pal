from datetime import datetime, timedelta

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QTableWidgetItem, QLabel

from app import APP


class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(1037, 742)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.pushButton = QtWidgets.QPushButton(self.centralwidget)
		self.pushButton.setGeometry(QtCore.QRect(380, 50, 171, 51))
		self.pushButton.setObjectName("pushButton")
		self.pushButton.clicked.connect(self.populate_tables)
		self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
		self.tableWidget.setGeometry(QtCore.QRect(150, 170, 321, 520))
		self.tableWidget.setObjectName("tableWidget")
		self.tableWidget.setColumnCount(0)
		self.tableWidget.setRowCount(0)
		self.tableWidget_2 = QtWidgets.QTableWidget(self.centralwidget)
		self.tableWidget_2.setGeometry(QtCore.QRect(530, 170, 321, 520))
		self.tableWidget_2.setObjectName("tableWidget_2")
		self.tableWidget_2.setColumnCount(0)
		self.tableWidget_2.setRowCount(0)
		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 1037, 26))
		self.menubar.setObjectName("menubar")
		self.menuStripe_google_calendar_poro_ilo = QtWidgets.QMenu(self.menubar)
		self.menuStripe_google_calendar_poro_ilo.setObjectName("menuStripe_google_calendar_poro_ilo")
		MainWindow.setMenuBar(self.menubar)
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)
		self.menubar.addAction(self.menuStripe_google_calendar_poro_ilo.menuAction())

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

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
		self.pushButton.setText(_translate("MainWindow", "Ustvari poročilo"))
		self.menuStripe_google_calendar_poro_ilo.setTitle(_translate("MainWindow", "Stripe & google calendar poročilo"))

	def populate_tables(self):
		APP.init()
		service = APP.use_case.ustvari_racunsko_porocilo()

		current_date = datetime.now().date()

		zacetek = current_date - timedelta(weeks=1)
		konec = current_date
		# zacetek = date(2023, 4, 1)
		# konec = date(2023, 5, 14)
		rp = service.exe(zacetek=zacetek, konec=konec)

		self.tableWidget.clearContents()

		row = 0
		self.tableWidget_2.setRowCount(len(rp.dnevi))
		column_labels = ["Začetek", "Konec", "Naslov inštrukcije", "Ime", "Email", "Email računa", "Telefonska"]
		self.tableWidget_2.setColumnCount(len(column_labels))
		self.tableWidget_2.setHorizontalHeaderLabels(column_labels)
		self.tableWidget.setRowCount(len(rp.dnevi))
		column_labels = ["Ime", "Email učenca", "Čas knjiženja", "Račun"]

		self.tableWidget.setColumnCount(len(column_labels))
		self.tableWidget.setHorizontalHeaderLabels(column_labels)

		for dnevno_rp in rp.dnevi:
			for element in dnevno_rp.elementi:
				if element.knjizni_vnos:

					name = element.knjizni_vnos.placnik.ime
					email = element.knjizni_vnos.placnik.email_racuna
					date = element.knjizni_vnos.datum
					date_str = date.strftime("%Y-%m-%d %H:%M:%S")
					racun_placan = "plačano" if element.knjizni_vnos.placano else "ni plačano"

					name_item = QTableWidgetItem(name)
					email_item = QTableWidgetItem(email)
					date_item = QTableWidgetItem(date_str)
					racun_item = QTableWidgetItem(racun_placan)

					self.tableWidget.setItem(row, 0, name_item)
					self.tableWidget.setItem(row, 1, email_item)
					self.tableWidget.setItem(row, 2, date_item)
					self.tableWidget.setItem(row, 3, racun_item)

					row += 1
				elif element.dogodek:

					zacetek_item = QTableWidgetItem(str(element.dogodek.zacetek))
					konec_item = QTableWidgetItem(str(element.dogodek.konec))
					naslov_item = QTableWidgetItem(element.dogodek.ime)
					ime_item = QTableWidgetItem(element.dogodek.uporabnik.ime)
					email_item = QTableWidgetItem(element.dogodek.uporabnik.email)
					email_racuna_item = QTableWidgetItem(element.dogodek.uporabnik.email_racuna)
					telefon_item = QTableWidgetItem(element.dogodek.uporabnik.telefon)

					self.tableWidget_2.setItem(row, 0, zacetek_item)
					self.tableWidget_2.setItem(row, 1, konec_item)
					self.tableWidget_2.setItem(row, 2, naslov_item)
					self.tableWidget_2.setItem(row, 3, ime_item)
					self.tableWidget_2.setItem(row, 4, email_item)
					self.tableWidget_2.setItem(row, 5, email_racuna_item)
					self.tableWidget_2.setItem(row, 6, telefon_item)

					row += 1

		self.tableWidget.resizeColumnsToContents()
		self.tableWidget.resizeRowsToContents()

		self.tableWidget_2.resizeColumnsToContents()
		self.tableWidget_2.resizeRowsToContents()


if __name__ == "__main__":
	import sys

	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())
