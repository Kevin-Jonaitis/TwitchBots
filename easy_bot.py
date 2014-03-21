import time
import socket #imports module allowing connection to IRC
import threading #imports module allowing timing functions
import sy



global irc


def setup():
	global irc
	password = sys.argv[2]
	botnick = sys.argv[1]
	channel = "twitchplayspokemon"
	#channel = "kevin117007"

	server = '199.9.252.26'
	irc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	irc.connect((server,6667))
	irc.send("Pass %s\n" % (password))
	irc.send("NICK %s\n" % (botnick))
	irc.send("JOIN #%s\n" % (channel))

def sendMessage(message):
	irc.send("PRIVMSG #%s :%s\n" % (channel, message))

def reconnect():
	global irc
	irc.close()
	irc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	irc.connect((server, 6667))
	irc.send("Pass %s\n" % (password))
	irc.send("NICK %s\n" % (botnick))
	irc.send("JOIN #%s\n" % (channel))


def loop():
	while True:
		try:
			ircmsg = irc.recv(1024)
		except Exception as e:
			print e
			reconnect()

		if not ircmsg:
			print ("It's not an ircmsg, but rather: " + str(ircmsg))
			try:
				reconnect()
			except Exception as e:
					print e

		if ircmsg.find('PING ') != -1:
				print "We got a ping!"
				print ircmsg
				irc.send('PING :PONG\n')

		#Private message to me, read it
		if ircmsg.find('PRIVMSG ' + botnick.lower()) != -1:
		print ircmsg	
	
		if ircmsg.find('PRIVMSG kevin117007') != -1:
        	        print ircmsg

		if ircmsg.find(' PRIVMSG ') != -1:
				nick = ircmsg.split('!')[0][1:]
				if(nick.lower() == 'kevin117007' or nick.lower() == 'me'):
					print("MESSAGE FROM USER SUCCESSFULLY SENT")
					print ircmsg
