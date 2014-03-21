import time
import socket #imports module allowing connection to IRC
import threading #imports module allowing timing functions
import sys

botnick = sys.argv[1]
password = sys.argv[2]
channel = "twitchplayspokemon"
server = '199.9.252.26'

global command_socket
global irc

def connect_irc():
	global irc
	irc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	irc.connect((server,6667))
	irc.send("Pass %s\n" % (password))
	irc.send("NICK %s\n" % (botnick))
	irc.send("JOIN #%s\n" % (channel))

def connect_command():
	global command_socket
	command_socket = socket.socket()
	command_socket.connect(('localhost',1234))
	print command_socket.getsockname()[1]
	print "Setting up a bot..."
	command_socket.send("bot")

def sendMessage(message):
	irc.send("PRIVMSG #%s :%s\n" % (channel, message))

connect_command()
connect_irc()

while True:
	#Reading from the Server
	try:
		servMessage = command_socket.recv(command_socket.getsockname()[1])
	except Except as e:
		print e
		connect_command()
		continue
        
	print botnick + " recieved: " + str(servMessage)
	try:
		sendMessage(servMessage)
       	except Exception as e:
		connect_irc()
		try:
			sendMessage(servMessage)
		except:
			print "Failed to send message from: " + botnick 
			pass
