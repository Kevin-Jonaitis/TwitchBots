import time
import socket #imports module allowing connection to IRC
import threading #imports module allowing timing functions
import sys

password = "oauth:2zpa8b87loa20xy7tttg4lp8r1clb5e"
botnick = "abbakadaba"

channel = "twitchplayspokemon"
#channel = "kevin117007"

server = '199.9.252.26'
#server = 'irc.twitch.tv'

irc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
irc.connect((server,6667))
irc.send("Pass %s\n" % (password))
irc.send("NICK %s\n" % (botnick))
irc.send("JOIN #%s\n" % (channel))

def sendMessage(message):
	print irc.send("PRIVMSG #%s :%s\n" % (channel, message))


while True:
	ircmsg = irc.recv(1024)

#	print ircmsg
#	print "\n\n\n\n"

	if not ircmsg:
		print ("it's not an ircmsg")
		try:
				irc.close()
				irc.connect((server, 6667))
		except Exception as e:
				print e

	if ircmsg.find('PING ') != -1:
			print "We got a ping!"#
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
