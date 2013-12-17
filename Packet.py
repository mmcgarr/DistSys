#/usr/bin/python
import json

class Packet:

	def __init__(self, type, node_id, from_ip_address, to_ip_address = none, data):
		self.type = type
		self.node_id = node_id
		self.from_ip_address = from_ip_address
		self.to_ip_address = to_ip_address
		self.data = data

		if type == "JOINING_NETWORK_SIMPLIFIED"
				

	def send(self, sock):
		print "sending"
		
		sock.sendto(json.dumps(self.__dict__), (self.to_ip_address, 8767))


class SearchResult:
	pass


