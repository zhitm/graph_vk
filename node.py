import numpy
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

		# physics attributes
		self.coords = numpy.array([0,0])
		self.velocity = numpy.array([0,0])
		self.accel = numpy.array([0, 0])

	def dict_upd(self):
		Node.id_node_dict.update({self.id: self})

	@staticmethod
	def id_to_node(node_id):
		if node_id in Node.id_node_dict:
			return Node.id_node_dict[node_id]
		else:
			return Node(node_id)

	def draw(self, view, pygame, screen):
		pygame.draw.circle(screen, (0, 0, 255), view.transform(self.coords[0], self.coords[1]), 30)
