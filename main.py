import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import requests

HEADINGS = ['AIRWAYS', 'AQUAMARINE', 'ARACHNOPHOBIA', 'ARCANE', 'ARCTIC', 'ASTEROID', 'AVALANCHE', 'BEEHIVE', 'BLOCKS', 'BOUNCE', 'CARS', 'CLOCKWORK', 'COLORS', 'COMET', 'CPU', 'DEEPER_AND_DEEPER', 'DEEP_SEA', 'DNA', 'DRAIN', 'ESCHER', 'FACTORY', 'FASTFOOD', 'FLOATLANDS', 'FUTURISTIC', 'GLITCH', 'GOLD_MINE', 'GOLD_RUSH', 'GRAVIBEE', 'GRAVITY_SPIRE', 'GREEN_HILL', 'HELL', 'HIGHWAY', 'HORROR', 'HYPNOSIS', 'KODIINTHUR', 'LAB', 'LANTERNS', 'LIBRARY', 'LUSH', 'MAGIC', 'MERIDIAN_TRENCH', 'METEOR', 'MINE', 'MOBS', 'NARNIA', 'NIGHTMARE', 'OCEAN', 'ORE', 'OVERGROWN', 'PACMAN', 'PANDA', 'PIPE', 'PIRATES', 'PIXEL', 'PLANTS', 'PRESENTS', 'PYRAMID', 'RAIN', 'REFLECTION', 'RHYTHM', 'RUINS', 'SHACKLED', 'SHAKER', 'SHROOMS', 'SPEARS', 'SWEETTOOTH', 'TETRIS', 'TOYS', 'TRAFFIC', 'TREES', 'TREETOP', 'TRON', 'VALFORD', 'VOLCANO', 'WARFARE', 'WAVE', 'WONDERLAND']


def formatHeading(data):
	return ' '.join([i[0].upper() + i[1:].lower() for i in data.split('_')])


def formatTime(time):
	time = str(time)
	if len(time) > 3:
		return time[:-3] + ":" + time[-3:]
	elif len(time) == 3:
		return "0:" + time
	elif len(time) == 2:
		return "0:0" + time
	elif len(time) == 1:
		return "0:00" + time
	else:
		return "0:000"


class Table(QTableWidget):
	def __init__(self, *args):
		QTableWidget.__init__(self, *args)
		self.playerData = "-1"
		while self.playerData == "-1":
			self.name, self.result = QInputDialog.getText(self, "Username Entry", "Please enter your minecraft username:")
			self.playerData = self.getPlayerData(self.name)
		self.WRData = self.getWRData()
		self.setData()
		self.resizeColumnsToContents()
		self.resizeRowsToContents()
		self.resize(400, 600)
		self.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
		self.setWindowTitle("HiveMC Gravity Speedrun Tool")
		self.finalData = []

	def setData(self):
		self.setHorizontalHeaderLabels(['You', 'WR', 'Difference'])
		self.setVerticalHeaderLabels([formatHeading(heading) for heading in HEADINGS])
		self.finalData = [{heading: "" for heading in HEADINGS}, {heading: "" for heading in HEADINGS}, {heading: "" for heading in HEADINGS}]
		for key, value in self.playerData.items():
			try:
				self.finalData[0][key] = formatTime(value)
			except KeyError:
				pass
		for key, value in self.WRData.items():
			try:
				self.finalData[1][key] = value
			except KeyError:
				pass
		for key in HEADINGS:
			try:
				self.finalData[2][key] = self.differenceOfTimes(self.finalData[0][key], self.finalData[1][key])
			except KeyError:
				pass
		for key in HEADINGS:
			self.setItem(HEADINGS.index(key), 0, QTableWidgetItem(self.finalData[0][key]))
			self.setItem(HEADINGS.index(key), 1, QTableWidgetItem(self.finalData[1][key]))
			self.setItem(HEADINGS.index(key), 2, QTableWidgetItem(self.finalData[2][key]))

	def differenceOfTimes(self, playerTime, wrTime):
		if wrTime != "" and playerTime != "":
			return formatTime(self.parseTime(playerTime) - self.parseTime(wrTime))
		else:
			return ""

	def refresh(self):
		self.playerData = self.getPlayerData(self.name)
		for key, value in self.playerData.items():
			try:
				self.setItem(HEADINGS.index(key), 0, QTableWidgetItem(formatTime(value)))
			except KeyError:
				pass

	@staticmethod
	def parseTime(time: str):
		return int(time.replace(":", ""))

	@staticmethod
	def getPlayerData(name):
		r = requests.get(f"https://api.hivemc.com/v1/player/{name}/GRAV")
		try:
			return r.json()['maprecords']
		except KeyError:
			return "-1"

	@staticmethod
	def getWRData():
		r = requests.get(f"https://www.speedrun.com/api/v1/games/o1y9kwv6/records?top=1&max=200")
		data = r.json()
		wrData = {}
		for dataPoint in data['data']:
			weblink = dataPoint['weblink']
			if weblink.find('Glitched') != -1:
				break
			subStrStart = weblink.find("hivemc_dropper") + 15
			substrEnd = weblink.find("Glitch") - 1
			currentGame = weblink[subStrStart:substrEnd].upper()
			wrData[currentGame] = str(dataPoint['runs'][0]['run']['times']['primary_t']).replace(".", ":")
		return wrData


class MainWindow(QMainWindow):
	def __init__(self, *args, **kwargs):
		super().__init__()
		self.initUI()

	def initUI(self):
		table = Table(len(HEADINGS), 3)
		table.show()
		self.setCentralWidget(table)

		exitAct = QAction(QIcon('exit.png'), '&Exit', self)
		exitAct.setShortcut('Ctrl+Q')
		exitAct.setStatusTip('Exit application')
		exitAct.triggered.connect(qApp.quit)

		self.statusBar()

		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(exitAct)

		self.move(300, 150)
		self.setWindowTitle('PyQt window')
		self.show()


def refreshClicked():
	global table
	table.refresh()


def main(args):
	global table
	app = QApplication(args)
	# table = Table(len(HEADINGS), 3)
	# table.show()
	# b1 = QPushButton(table)
	# b1.setText("Refresh Stats")
	# b1.clicked.connect(refreshClicked)
	# b1.show()
	_ = MainWindow()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main(sys.argv)
