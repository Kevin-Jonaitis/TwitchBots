from pymongo import MongoClient
client = MongoClient(host='kevinjonaitis.com')
print client.alive()
twitch_db =  client.twitch
twitch_db.authenticate('Twitch', password='123456')
bots = client.twitch.bots
print bots.find_one()

#bot = {"username" : "botty","password" : "pass","email" : "email@kevinjonaitis.com", "oauth" : "sdflkjdslkj34lkjsdflkj34lkjs" }
#bots.insert(bot)
#cursor =  bots.find()
#for bot in cursor:
#	print bot


def addUser(username,password,email):
	client = MongoClient(host='kevinjonaitis.com')
	twitch_db =  client.twitch
	twitch_db.authenticate('Twitch', password='123456')
	bots = client.twitch.bots
	bot = {"username" : username, "password" : password, "email" : email }
	bots.insert(bot)
