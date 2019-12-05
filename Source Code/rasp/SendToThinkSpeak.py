import sys
import urllib.request  as urllib2


# Enter Your API key here
myAPI = 'MHSRHH0QT1ANG75R' 
myAPI2 = '1LSNZSQNM1Z7E5KG'
# URL where we will send the data, Don't change it
baseURL = 'https://api.thingspeak.com/update?api_key=%s'% myAPI 
baseURL2 = 'https://api.thingspeak.com/update?api_key=%s'% myAPI2 

def ThingSpeak_admin_begin(buf):
	try: 
		msg = buf
		#print(msg)
		#Sending the data to thingspeak
		conn = urllib2.urlopen(baseURL + msg)
		print(conn.read())
		conn.close()
		print("OK")
		return
	except:
		print("ENOR SEND DATA")
      
def ThingSpeak2_admin_begin(buf):
	try: 
		msg = buf
		#print(msg)
		#Sending the data to thingspeak
		conn = urllib2.urlopen(baseURL2 + msg)
		print(conn.read())
		conn.close()
		print("OK")
		return
	except:
		print("ENOR SEND DATA")
