from subprocess import call
import urllib2
import time

class IPReset:
	def __init__(self,port,adb_path):
		self.port = port
		self.adb_path = adb_path

		# Set up proxy through phone
		proxy = urllib2.ProxyHandler({'http': 'localhost:' + str(self.port)})
                opener = urllib2.build_opener(proxy)
                urllib2.install_opener(opener)

	def initalize_ip(self):
		print "Initalizing IP..."
		try:
			self.ip =  urllib2.urlopen('http://myip.dnsdynamic.org/').read()
		except Exception as e:
			print e
			print ("Could not estabilish connection to ip checker site. Please check your internet conneciton and try again")
			exit()
		print "Initial IP: " + str(self.ip)

	def reset_ip(self):
		print "Resetting ip..."
		ext_ip =  urllib2.urlopen('http://myip.dnsdynamic.org/').read()
		path = [self.adb_path,"shell","am","startservice","--user","0","-n","com.example.datatoggler/.DataToggler"]
		call(path)

		# Check external ip checker to see if ip changed
		while (ext_ip == self.ip):
			try:
				ext_ip = urllib2.urlopen('http://myip.dnsdynamic.org/').read()
			except Exception as e:
				pass
			time.sleep(1)
		self.ip = ext_ip #update the ip
		print "New ip: " + str(self.ip)
