import irc.bot as ib
import time,random,characters,codecs

def getPassword():
	with open("password.txt") as f:
		return f.read().strip()

def getEffect(char,a):
	if a=="weapon":
		return char.damage
	else:
		return char.defence

def getType(a):
	if a=="weapon":
		return "Damage"
	else:
		return "Defence"

def log(nick,message):
	with codecs.open("www/log.txt","a","utf-8") as f:
		f.write(u"{} {}: {}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"),nick,message))

class DnDBot(ib.SingleServerIRCBot):
	def __init__(self,chans,nickname,server,port=6667):
		ib.SingleServerIRCBot.__init__(self,[(server,port)],nickname,nickname)
		self.chanlist = chans
		self.bot_nick = nickname

	def on_welcome(self,c,e):
		c.privmsg("NickServ","identify "+getPassword())
		for channel in self.chanlist:
			c.join(channel)

	def on_pubmsg(self,c,e):
		self.on_message(c,e)

	def on_privmsg(self,c,e):
		self.on_message(c,e)

	def say(self,c,e,text):
		c.privmsg(e.target,text)
		log(self.bot_nick,text)

	def on_message(self,c,e):
		text = e.arguments[0].strip()
		nick = e.source.nick
		log(nick,text)
		if text=="!aboutme":
			self.say(c,e,"I am ImANoob's DnD IRC bot, rewritten in Python because fuck Java and fuck not having good uptime.")
		if text=="!src":
			self.say(c,e,"The source code for DnDBot is at https://github.com/MineRobber9000/DnDBot")
		if text.startswith("!roll "):
			parts = text.split()
			parts.pop(0)
			results = []
			for die in parts:
				try:
					nparts = [int(p) for p in die.split("d")]
					for i in xrange(nparts[0]):
						results.append(random.randint(1,nparts[1])+1)
				except ValueError as e:
					pass
			self.say(c,e,"You rolled a {!s}. [{}]".format(sum(results),"+".join([str(r) for r in results])))
		if text.startswith("!character"):
			parts = text.split()
			if not characters.exists(parts[1]):
				self.say(c,e,"{}: Who's {}?".format(nick,parts[1]))
				return
			char = characters.getChar()
			a = parts[2].lower()
			if not hasattr(char,a):
				self.say(c,e,"{}: I don't know that about {}.".format(nick,parts[1]))
			attr = getattr(char,a)
			if type(attr)==str and a not in ("weapon","armor"):
				self.say(c,e,"{}: {}".format(nick,attr))
			else:
				if a=="health":
					self.say(c,e,"{0}: {1}'s health is at {2[0]}/{2[1]}".format(nick,parts[1],attr))
				elif a in ("offhand","slung","worn"):
					self.say(c,e,"{0}: {1}'s {2} effect is {3[0]} (a {3[1]} effect)".format(nick,parts[1],a,attr))
				elif a in ("weapon","armor"):
					self.say(c,e,"{}: {}'s {}s effect is {} (a {} effect)".format(nick,parts[1],attr,getEffect(a),getType(a)))
				elif a=="anima":
					self.say(c,e,"{0}: {1}'s anima is at {2[0]}/{2[1]}".format(nick,parts[1],attr))
				elif a=="items":
					attr = filter(None,attr)
					self.say(c,e,"{}: {} has: {}".format(nick,parts[1],",".join(attr)))

if __name__=="__main__":
	bot = DnDBot(["#dnd"],"DnDBot","irc.badnik.zone")
	bot.start()
