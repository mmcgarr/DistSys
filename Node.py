#/usr/bin/python

import json
from Packet import Packet
import math 
from socket import *
import threading

HOST = "127.0.0.1"
PORT = 8767
MESSAGE = "OMG HI"

class Node:
	def __init__(self, node_id):
		self.node_id = node_id
		self.routing_table = ([])
		
		self.sendSock = socket(AF_INET, SOCK_DGRAM)
		self.recieve()
		print "done with receiving"
		self.join()
		
	def join(self):
		print 'joining'
		p = Packet("JOINING_NETWORK_SIMPLIFIED", self.node_id, "127.0.0.1", "")
		p.send(self.sendSock)

	def leave(self):
		pass

	def hashCode(self, str):
		hash = 0
		for c in str:
			hash = hash *31 + ord(c)

		return math.fabs(hash)

	def listenAndRespond(self):
		s = socket(AF_INET, SOCK_DGRAM)
		s.bind((HOST,PORT))
		addr = (HOST,PORT)
		while True:
			data, addr = s.recvfrom(1024)
			packet = json.loads(data)
			if packet["type"] == "JOINING_NETWORK_SIMPLIFIED":
				print "Add node to routing table"
				self.routing_table.append((packet["node_id"], packet["from_ip"]))
				print self.routing_table


	def recieve(self):
		t = threading.Thread(target = self.listenAndRespond)
#		t.daemon = True
		t.start()




def main():
	Node(42)


if __name__ == "__main__":
	main()
