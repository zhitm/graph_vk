from node import Node
from collections import deque
from itertools import combinations
import pygame

C = 15000
K = 1
M = 1

class Graph:
	def __init__(self):
		self.nodes = set()
		self.graph = {}
		self.node_cnt = 0
		self.is_connected = True
	def add_node(self, id):
		node = Node.id_to_node(id)
		self.nodes.add(node)
		self.graph.update({node: node.friends})
		self.node_cnt += 1
		Node.id_node_dict.update({id: node})
	def add_edge(self, node1, node2):
		node1.friends.add(node2)
		node2.friends.add(node1)
		self.graph.update({node1: node1.friends})
		self.graph.update({node2: node2.friends})

	def del_edge(self, node1, node2):
		node1.friends.discard(node2)
		node2.friends.discard(node1)
		self.graph.update({node1: node1.friends})
		self.graph.update({node2: node2.friends})

	def del_node(self, node):
		if node in self.nodes:
			self.nodes.remove(node)
		for friend in node.friends:
			friend.friends.discard(node)
			self.graph.update({friend: friend.friends})
		self.graph.pop(node)

	def go_in_depth(self, node):
		node.used = True
		for vert in node.friends:
			if vert.used == False:
				self.go_in_depth(vert)

	def go_in_width(self, start_node):
		q = deque()
		q.append(start_node)
		while q:
			vert = q.popleft()
			vert.used = True
			for next in vert.friends:
				if next.used == False:
					q.append(next)
					next.used = True
		for node in self.nodes: #возращаем исходные значения для следующего обхода
			node.used = False

	def set_node_coords(self, node, x, y):
		node.coords[0] = x
		node.coords[1] = y

	#physics
	def apply_force(self):  # be careful, forces must be set to zero somewhere!!!
		for pair in combinations(self.nodes, 2):
			fst = pair[0]
			scnd = pair[1]
			dist = ((fst.coords[0] - scnd.coords[0]) ** 2 + (fst.coords[1] - scnd.coords[1]) ** 2) ** 0.5
			if(dist != 0):
				coulomb_force = (fst.coords - scnd.coords) * (C / (dist ** 2))
				fst.accel += coulomb_force
				scnd.accel -= coulomb_force
				if (scnd in fst.friends):
					hooke_force = K * (fst.coords - scnd.coords)
					fst.accel -= hooke_force
					scnd.accel += hooke_force

	def move(self, delta_t):
		for node in self.nodes:
			node.velocity += node.accel * delta_t
			node.coords += node.velocity * delta_t
			node.accel = (0,0)  # set to zero
			#energy dissipation
			node.velocity /= 1.01

	def draw(self, view, pygame, screen):
		for pair in combinations(self.nodes, 2):
			if pair[0] in pair[1].friends:
				pygame.draw.line(screen, (0, 0, 0), view.transform(pair[0].coords[0], pair[0].coords[1]),
							 view.transform(pair[1].coords[0], pair[1].coords[1]))

		for node in self.nodes:
			node.draw(view, pygame, screen)

if __name__ == '__main__':
	g = Graph()
	file = open('members.txt', 'r')
	for line in file:
		line = line.strip()
		arr = line.split()
		id = arr[0]
		g.add_node(id)
		node = Node.id_to_node(id)
		for friend_id in arr[1:]:
			node = Node.id_to_node(id)
			friend = Node.id_to_node(friend_id)
			g.add_edge(node, friend)
