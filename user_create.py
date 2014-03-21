from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.proxy import *

#For system calls
from subprocess import call
from subprocess import Popen
from sys import platform as _platform

import time
from ip_reset import *

def create_user(browser,name,passwrd,eml):
	#browser = webdriver.Firefox()
	browser.get('http://www.twitch.tv/signup')
	
	#time.sleep(2)

	username = browser.find_element_by_id('user_login')
	username.send_keys(name)

	password = browser.find_element_by_id('user_password')
	password.send_keys(passwrd)

	password = browser.find_element_by_id('user_email')
	password.send_keys(eml)

	month_selector = browser.find_element_by_id('date_month')
	months = month_selector.find_elements_by_tag_name("option") #grab the first element
	months[1].click()

	day_selector = browser.find_element_by_id('date_day')
	days = day_selector.find_elements_by_tag_name("option") #grab the first element
	days[1].click()

	year_selector = browser.find_element_by_id('date_year')
	years = year_selector.find_elements_by_tag_name("option") #grab the first element
	years[1].click()

	recaptcha = browser.find_element_by_id('recaptcha_response_field')
	recaptcha.click()

	# Using a while loop, because there are no listerns for user events
	signedUp = False
	while(not signedUp):
		if(browser.current_url == "http://www.twitch.tv/"):
			signedUp = True
			print "Created user: " + str(name)
			browser.delete_all_cookies()
		time.sleep(1)
	print "We are done with this user signup"


#server : the name of the selenium server we will be running
def create_users(basename,starting_number,ending_number,password,useProxy,port='8080',selenium_server_path='',adb_path=''):
	global ip #Used to reset the ip
	if(useProxy):
		executed = False
		result = Popen(["java","-jar",selenium_server_path,"&"]) # Starts the selenium server
		if (_platform == "darwin" or _platform == "linux" or _platform == "linux2"):
			result = call(["./" + str(adb_path),"forward","tcp:" + str(port),"tcp:" + str(port)]) #Linux adb run
		else: #It's windows
			result = call(["/" + str(adb_path),"forward","tcp:" + str(port),"tcp:" + str(port)]) #Windows adb run
		
		if(result == 0):
			print "Successfully ran ADB"
		else:
			print "ERROR ERROR ERROR PROBLEM WITH RUNNING ADB. Return Error code: " + str(result)
			print "Exiting..."
			exit()

		myProxy = "localhost:" + str(port)
		proxy = Proxy({
    			'proxyType': ProxyType.MANUAL,
    			'httpProxy': myProxy,
    			'ftpProxy': myProxy,
    			'sslProxy': myProxy,
    			'noProxy': 'localhost,127.0.0.1' # set this value as desired
    				})
		# for remote
        	caps = webdriver.DesiredCapabilities.FIREFOX.copy()
        	proxy.add_to_capabilities(caps)
        	browser = webdriver.Remote(desired_capabilities=caps)
	else:
		browser = webdriver.Firefox()

        wait = ui.WebDriverWait(browser,10) #Wait for 10 seconds for elements to appear
	
	reseter = IPReset(port,adb_path)
	reseter.initalize_ip()
#	reseter.reset_ip()
#       reseter.reset_ip()
#        reseter.reset_ip()
#        reseter.reset_ip()

	counter = 0 ; #Reset the counter after ever 2 users are created. 
        for i in range(starting_number,ending_number):
		try:
			if (counter >= 2):
				counter = 0;
				reseter.reset_ip()
	               	create_user(browser, basename + str(i),password, basename + str(i) + "@kevinjonaitis.com")
			counter = counter + 1
		except Exception as e:
			print e
			print "Could not create user: " + str(basename + str(i))
		#time.sleep(30) # We have to wait 30 sceonds to prevent being rate limited by twitch
        browser.quit()

create_users("botspammer",33,37,'12345',True,"8085","selenium-server-standalone-2.40.0.jar","android-development/sdk/platform-tools/adb")
