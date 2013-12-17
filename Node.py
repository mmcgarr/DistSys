#/usr/bin/python

import json
from Packet import Packet
import math 
from socket import *


PORT = 8767
MESSAGE = "OMG HI"

class Node:
	def __init__(self, node_id):
		self.node_id = node_id
		
		self.sock = socket(AF_INET, SOCK_DGRAM)
		self.join()
		
	def join(self):
		p = Packet("JOINING_NETWORK_SIMPLIFIED", self.node_id, "127.0.0.1", "")
		p.send(self.sock)

	def leave(self):
		pass

	def hashCode(self, str):
		hash = 0
		for c in str:
			hash = hash *31 + ord(c)

		return math.fabs(hash)

def main():
	Node(42)


if __name__ == "__main__":
	main()
