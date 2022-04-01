from PyQt5.QtWidgets import (
	QApplication,
	QWidget,
	QMainWindow,
	QPushButton,
	QLineEdit,
	QLabel,
	QMessageBox,
)

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices

import requests
import sys
import webbrowser
import json

class MainWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		self.setWindowTitle("Client")
		self.setFixedSize(400, 400)
		
		self.label1 = QLabel("Enter your IP:", self)
		self.label1.move(10, 0)

		self.text1 = QLineEdit(self)
		self.text1.move(10, 30)

		self.label2 = QLabel("Enter your API Key:", self)
		self.label2.move(10, 60)

		self.text2 = QLineEdit(self)
		self.text2.move(10, 90)

		self.label3 = QLabel("Enter the hostname:", self)
		self.label3.move(10, 120)

		self.text3 = QLineEdit(self)
		self.text3.move(10, 150)

		self.button = QPushButton("Send", self)
		self.button.move(10, 180)

		self.button.clicked.connect(self.on_click)
		self.show()

	def on_click(self):
		my_ip = self.text1.text()
		API_key = self.text2.text()
		hostname = self.text3.text()

		if(my_ip == "") or (API_key == "") or (hostname == "") :
			QMessageBox.about(self, "Error", "Please fill the field")
		else:
			res = self.__query(my_ip, API_key, hostname)

			if res:
				lat = str(res.get('Latitude'))
				long = str(res.get('Longitude'))

				webbrowser.open(url="https://www.openstreetmap.org/?mlat=" + lat + "&mlon=" + long + "#map=12")
				self.close()

	def __query(self, my_ip, API_key, hostname):
		url = "http://" + hostname + "/ip/" + my_ip + "?key=" + API_key
		r = requests.get(url, timeout = 5)

		if r.status_code == requests.codes.NOT_FOUND:
			QMessageBox.about(self, "Error", "IP not found")

		if r.status_code == requests.codes.OK:
			return r.json()


if __name__ == "__main__":
	app = QApplication(sys.argv)
	main = MainWindow()
	app.exec_()