import irc.bot as ib

def getPassword():
	with open("password.txt") as f:
		return f.read().strip()

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

	def on_message(self,c,e):
		text = e.arguments[0].strip()
		if text=="!aboutme":
			c.privmsg(e.target,"I am ImANoob's DnD IRC bot, rewritten in Python because fuck Java and fuck not having good uptime.")

if __name__=="__main__":
	bot = DnDBot(["#dnd"],"DnDBot","irc.badnik.zone")
	bot.start()
