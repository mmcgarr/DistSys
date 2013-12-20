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
	def __init__(self, node_id, ip_addr):
		self.node_id = node_id
		self.routing_table = ([(1, "1.1.1.1"), (2, "2.2.2.2"), (5, "5.5.5.5"), (8, "8.8.8.8")])

		self.ip = ip_addr
		
		self.sendSock = socket(AF_INET, SOCK_DGRAM)
		self.recieve()
		print "done with receiving"
		self.join()
		
	def join(self):
		print 'joining'
		p = Packet("JOINING_NETWORK_SIMPLIFIED", node_id=self.node_id+5, target_id = 2, from_ip="127.0.0.1")
		p.send(self.sendSock, "127.0.0.1")

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
#		while True:
		data, addr = s.recvfrom(1024)
		print data
		packet = json.loads(data)
		if packet["type"] == "JOINING_NETWORK_SIMPLIFIED":
			print "Add node to routing table"
			self.routing_table.append((packet["node_id"], packet["from_ip"]))
			print self.routing_table
			if self.node_id != packet["target_id"]:
				closest = self.findClosestNode(packet["target_id"])
				print closest
				for i,v in self.routing_table:
					if i == closest:
						break
				Packet("JOINING_NETWORK_SIMPLIFIED", node_id=packet["node_id"], target_id=packet["target_id"], from_ip="127.0.0.1").send(self.sendSock, v)
				print 'sending packet on to ' + v 
				

	def findClosestNode(self, target_id):
		print 'finding closest'
		max = 0
		for (id,ip) in self.routing_table:
			if id <= target_id and id > max:
				max = id
		if self.node_id > max and self.node_id < target_id:
			max = self.node_id

		return max

		

	def recieve(self):
		t = threading.Thread(target = self.listenAndRespond)
#		t.daemon = True
		t.start()




def main():
	Node(7, "7.7.7.7")


if __name__ == "__main__":
	main()
