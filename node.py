import numpy
from collections import defaultdict

NODE_RADIUS = 3

"""
Класс вершины графа
"""
class Node:
	id_node_dict = {}
	cnt = 0
	def __init__(self, id):
		self.id = id
		self.degree = 0
		self.friends = set()
		self.used = False #переменная для обходов, сразу после обхода превращается обратно в False
		self.number = Node.cnt
		Node.id_node_dict.update({self.id: self})
		Node.cnt += 1

		# используются преимущественно в лувенском алгоритме (вероятно, только в нем)
		self.current_group = None
		self.eaten_ids = {self.id}
		self.friends_lv = defaultdict(int)  # словарь ребро (вершина, с которой связана self) : вес ребра

		# физические параметры вершины
		self.coords = numpy.array([0,0], dtype=numpy.float64)
		self.velocity = numpy.array([0,0], dtype=numpy.float64)
		self.accel = numpy.array([0, 0], dtype=numpy.float64)



	def cnt_degree(self):
		self.degree = len(self.friends)

	@staticmethod
	def id_to_node(node_id):
		return Node.id_node_dict.get(int(node_id))

	@staticmethod
	def set_node_coords(node, x, y):
		node.coords[0] = x
		node.coords[1] = y

	def draw(self, view, pygame, screen):
		pygame.draw.circle(screen, (0, 0, 255), view.transform(self.coords[0], self.coords[1]), NODE_RADIUS)