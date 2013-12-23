#/usr/bin/python

import json
from Packet import * 
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
		self.url = ([])

		self.ip = ip_addr
		
		self.sendSock = socket(AF_INET, SOCK_DGRAM)
		self.recieve()
		print "done with receiving"
		self.join()
		self.index()
		self.leave()
		
	def join(self):
		print 'joining'
		p = Packet("JOINING_NETWORK_SIMPLIFIED", node_id=self.node_id+5, target_id = 2, from_ip="127.0.0.1")
		p.send(self.sendSock, "127.0.0.1")

	def index(self):
		print 'indexing'
		p = Packet('INDEX', target_id=self.node_id, sender_id=self.node_id, keyword="Abba", link=["domain.com"])
		p.send(self.sendSock, "127.0.0.1")

	def leave(self):
		print 'leaving network'
		p = Packet('LEAVING_NETWORK', node_id=8)
		for _,ip in self.routing_table:
			print ip
			p.send(self.sendSock, ip)

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
			print data
			packet = json.loads(data)
			if packet["type"] == "JOINING_NETWORK_SIMPLIFIED":
				print "Add node to routing table"
				self.routing_table.append((packet["node_id"], packet["from_ip"]))
				print self.routing_table
				if self.node_id != packet["target_id"]:
					closest_id, closest_ip = self.findClosestNode(packet["target_id"])
					print closest_id
					Packet("JOINING_NETWORK_RELAY_SIMPLIFIED", node_id=packet["node_id"], target_id=packet["target_id"], gateway_id=self.node_id).send(self.sendSock, closest_ip)
					print 'sending packet on to ' + closest_ip 
			elif packet["type"] == "JOINING_NETWORK_RELAY_SIMPLIFIED":
				p = Packet("ROUTING_INFO", gateway_id = packet["gateway_id"], node_id = packet["node_id"], from_ip = self.ip, route_table = self.routing_table) 
				_, closest_ip = findClosestNode(packet["gateway_id"])
				p.send(self.sendSock, closest_ip)
			elif packet["type"] == "INDEX": 
				print "Adding index"
				if packet["target_id"] == self.node_id:
					print "actually adding to this node's links"
					self.url.append(packet["link"])
					print self.url
				else:
					_, closest_ip = findClosestNode(packet['target_id'])
					Packet("INDEX", node_id=packet["sender_id"], target_id=packet["target_id"], keyword=packet["keyword"], link=packet['link']).send(self.sendSock, closest_ip)
			elif packet["type"] == "LEAVING_NETWORK": 
				print "received a leaving packet"
				print "current routing table"
				print self.routing_table

				for id,ip in self.routing_table:
					if id == packet["node_id"]:
						self.routing_table.remove((id, ip))
						break
				print self.routing_table
		print "**************************************************************"

	def findClosestNode(self, target_id):
		print 'finding closest'
		max = 0
		closest_ip = ""
		for (id,ip) in self.routing_table:
			if id <= target_id and id > max:
				max = id
				closest_ip = ip
		if self.node_id > max and self.node_id < target_id:
			max = self.node_id
			closest_ip = "127.0.0.1"
		return (max, closest_ip)

	def recieve(self):
		t = threading.Thread(target = self.listenAndRespond)
		#t.daemon = True
		t.start()

def main():
	Node(7, "7.7.7.7")

if __name__ == "__main__":
	main()
