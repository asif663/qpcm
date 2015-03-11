from httplib2 import Http
from urllib import urlencode
h = Http()
from sys import stdin, exc_info
from time import sleep
import datetime
import socket
import MySQLdb
from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import *
from smartcard.CardType import ATRCardType
from smartcard.CardRequest import CardRequest
from smartcard.util import toHexString, toBytes
#import serial, binascii
import win32api; 
import win32ui
from uuid import getnode as get_mac
# import easygui
# x = conn.cursor()                  
				 
class printobserver(CardObserver):
	def update(self, observable, (addedcards, removedcards)):
		cr = CardRequest(timeout=100000000000, newcardonly=True)
		cs = cr.waitforcard()
		cs.connection.connect()
		response, sw1, sw2 = cs.connection.transmit([0xFF, 0xCA, 0x00, 0x00, 0x00])
		self.tagid = toHexString(response).replace(' ','')
		id = self.tagid
		# print "ID ID THIS",id
		c=id.lower()
		# print c
		d=socket.gethostbyname(socket.gethostname())
		now = datetime.datetime.now()
		
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		# s.connect(("gmail.com",80))
		# ip = (s.getsockname()[0])
		# print ip
		mac = get_mac()
		print mac
		s.close()

		res = h.request("http://192.168.1.57:8000/get_club?mac="+str(mac), "GET")

		# print res[1]

		resp, content = h.request("http://192.168.1.57:8000/rfid_post?rfid="+str(c)+"&cid="+str(res[1]), "GET")

		print resp

		# query = ("select id from qpcmms_club where ip='%s'"%(mac))
		# x.execute(query)
		# result = [item[0] for item in x.fetchall()]
		# c_id = result[0]



		
# data = dict(id_poster="some_poster_id", id_content="some_content")
# resp, content = h.request("http://192.168.1.11:8000/rfid_post?rfid=1234&cid=8", "GET")

# print resp



		import time
		for i in range(len(id)):
			test = ord(id[i])
			win32api.keybd_event(test, i, )
		cs.connection.disconnect()
try:
	cardmonitor = CardMonitor()
	cardobserver = printobserver()
	cardmonitor.addObserver(cardobserver)
	import sys
	if 'win32' == sys.platform:
		print 'press Enter to continue'
		sys.stdin.read(1)
except:
	print exc_info()[0], ':', exc_info()[1]