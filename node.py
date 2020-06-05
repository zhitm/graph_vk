class Node:
	id_node_dict = {}
	def __init__(self, id):
		self.id = id
		self.friends = set()
		self.used = False #переменная для обходов, сразу после обхода превращается обратно в False
		self.number = None
		self.dict_upd()

	def dict_upd(self):
		Node.id_node_dict.update({self.id: self})

	def id_to_node(node_id):
		node = Node.id_node_dict.get(node_id)
		return node
