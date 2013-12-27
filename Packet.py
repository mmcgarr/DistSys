#/usr/bin/python
import json

class Packet:

	def __init__(self, type, node_id=None, from_ip = None, to_ip = None, gateway_id = None, route_table = None, target_id = None, link = None, keyword = None, sender_id = None, response = None, word = None):
		self.type = type

		if type == "JOINING_NETWORK_SIMPLIFIED":
			self.node_id = node_id
			self.target_id = target_id
			self.from_ip = from_ip
		elif type == "JOINING_NETWORK_RELAY_SIMPLIFIED":
			self.node_id = node_id
			self.target_id = target_id
			self.gateway_id = gateway_id
		elif type == "ROUTING_INFO":
			self.gateway_id = gateway_id
			self.node_id = node_id
			self.ip_address = from_ip
			self.table = route_table
		elif type == "LEAVING_NETWORK":
			self.node_id = node_id
		elif type == "INDEX":
			self.target_id = target_id
			self.sender_id = sender_id
			self.keyword = keyword
			self.link = link
		elif type == "SEARCH":
			self.word = word
			self.node_id = node_id
			self.sender_id = sender_id
		elif type == "SEARCH_RESPONSE":
			self.word = word
			self.node_id = node_id
			self.sender_id = sender_id
			self.response = response

	def send(self, sock, ip):
		print "sending"
		sock.sendto(json.dumps(self.__dict__), (ip, 8767)) 

