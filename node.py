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
		self.loop = 0
		self.eaten_nodes = {self} #для объединения вершин

		# physics attributes
		self.coords = numpy.array([0,0], dtype=numpy.float64)
		self.velocity = numpy.array([0,0], dtype=numpy.float64)
		self.accel = numpy.array([0, 0], dtype=numpy.float64)

	def dict_upd(self):
		Node.id_node_dict.update({self.id: self})

	@staticmethod
	def id_to_node(node_id):
		return Node.id_node_dict.get(node_id)

	def set_node_coords(node, x, y):
		node.coords[0] = x
		node.coords[1] = y
		print(node.coords)

	def draw(self, view, pygame, screen):
		pygame.draw.circle(screen, (0, 0, 255), view.transform(self.coords[0], self.coords[1]), 3)