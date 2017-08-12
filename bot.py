import irc.bot as ib
import time,random,os.path

def getPassword():
	with open("password.txt") as f:
		return f.read().strip()

def log(nick,message):
	with open("www/log.txt","a") as f:
		f.write("{} {}: {}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"),nick,message))

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
		log(e.source.nick,text)
		if text=="!aboutme":
			self.say(c,e,"I am ImANoob's DnD IRC bot, rewritten in Python because fuck Java and fuck not having good uptime.")
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
			print("NYI")

if __name__=="__main__":
	bot = DnDBot(["#dnd"],"DnDBot","irc.badnik.zone")
	bot.start()
