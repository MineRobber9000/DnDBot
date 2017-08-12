chars = []
import requests,csv
from cStringIO import StringIO

class Character:
	def __init__(self,row):
		self.name = row[0]
		self.player = row[1]
		self.classdata = row[2:3]
		self.race = row[4]
		self.age = row[5]
		self.xp = row[6]
		self.level = row[7]
		self.gender = row[8]
		self.height = row[9]
		self.weight = row[10]
		self.weapon = row[11]
		self.damage = row[12]
		self.armor = row[13]
		self.defence = row[14]
		self.offhand = row[15:17]
		self.slung = row[18:20]
		self.worn = row[21:23]
		self.items = row[25:35]
		self.copper = row[36]
		self.silver = row[37]
		self.gold = row[38]
		self.strength = row[39]
		self.dexterity = row[40]
		self.constitution = row[41]
		self.intelligence = row[42]
		self.health = row[43:44]
		self.anima = row[45:46]
		self.earnedxp = row[47]

def update():
	global chars
	chars = []
	csvtext = requests.get("https://docs.google.com/spreadsheets/d/1N0W_ZPhgJChHfGe5wFBRyvXgAoQ22t15cCbwPAsrZs0/export?format=csv").text
	reader = csv.reader(StringIO(csvtext))
	chardata = list(reader)
	chardata.pop(0)
	for row in chardata:
		chars.append(Character(row))

def exists(character):
	for char in chars:
		if char.name.startswith(character):
			return True
	return False

def getChar(character):
	if not exists(character):
		return False
	for char in chars:
		if char.name.startswith(character):
			return char
	return False

update()
