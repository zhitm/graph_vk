class Node:
	id_node_dict = {}
	cnt = 0
	def __init__(self, id):
		self.id = id
		self.friends = set()
		self.used = False #переменная для обходов, сразу после обхода превращается обратно в False
		self.number = Node.cnt
		self.dict_upd()
		Node.cnt += 1

	def dict_upd(self):
		Node.id_node_dict.update({self.id: self})
		
	def set_node_coords(node, x, y):
		node.coords[0] = x
		node.coords[1] = y
		print(node.coords)

	@staticmethod
	def id_to_node(node_id):
		if node_id in Node.id_node_dict:
			return Node.id_node_dict[node_id]
		else:
			return Node(node_id)
	
