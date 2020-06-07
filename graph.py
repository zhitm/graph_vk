from node import Node
from collections import deque
from itertools import combinations
from copy import deepcopy
import threading
import pygame

C = 15000 #что значат эти переменные?
#это физические константы. Использую их в apply_force ()
K = 1
M = 1

class Graph:
	def __init__(self):
		self.nodes = set() 
		self.graph = {} #contains pairs (node : set of its friends)
		self.groups = set() #please, write the type of data this set will contain
		self.node_cnt = 0
		self.load_graph() #specifically from file "member.txt"
		self.set_groups()


	def add_node(self, id):
		# what about self.groups? should it not be updated here?
		node = Node(id) #we might create another node with same id, even though we should not.
				#maybe  node = Node.id_to_node(id) ?
		self.nodes.add(node)
		self.graph.update({node: node.friends})
		self.node_cnt += 1 #this must not be incremented if we add an already existing element
		Node.id_node_dict.update({id: node}) #it will be updated in a constuctor fron Node.id_to_node(id), if the id was never
							#met before
		return node

	def add_edge(self, node1, node2):
		if node1 not in self.nodes or node2 not in self.nodes:
			print('in add_egde one of your nodes not in self.nodes')
			while True:
				pass
		node1.friends.add(node2)
		node2.friends.add(node1)
		self.graph.update({node1: node1.friends})
		self.graph.update({node2: node2.friends})

	def del_edge(self, node1, node2):
		if node1 not in self.nodes or node2 not in self.nodes or node2 not in node1.friends:
			print('in del_egde: this edge doesnt exist')
			while True:
				pass
		node1.friends.discard(node2)
		node2.friends.discard(node1)
		self.graph.update({node1: node1.friends})
		self.graph.update({node2: node2.friends})

	def del_node(self, node):
		# what about self.node_cnt ?
		if node in self.nodes:
			self.nodes.discard(node)
		else:
			print('in del_node you are trying to delete node what not exist')
			while True:
				pass
		for friend in node.friends:
			friend.friends.discard(node)
			self.graph.update({friend: friend.friends})
		self.graph.pop(node)

	def weight_cnt(self, node1, node2): #масса ребра между группами
		cnt = 0
		for node in node1.eaten_nodes:
			for eaten_by_node2 in node2.eaten_nodes:
				if node in eaten_by_node2.friends:
					cnt += 1
		return cnt

	def loop_cnt(self, node):
		cnt = 0
		for pair in combinations(node.eaten_nodes, 2):
			if pair[0] in pair[1].friends:
				cnt += 1

	def merge_nodes(self, node1, node2): #объединение
		# node_cnt ?
		node1.eaten_nodes += node2.eaten_nodes
		node2.eaten_nodes.clear()
		self.groups.discard(node2)

	def go_in_depth(self, node):
		node.used = True
		for vert in node.friends:
			if vert.used == False:
				self.go_in_depth(vert)
				vert.used = True
		for node in self.nodes: #возращаем исходные значения для следующего обхода
			node.used = False


	def go_in_width(self, start_node):
		ans = True

		q = deque()
		q.append(start_node)
		while q:
			vert = q.popleft()
			vert.used = True
			for next in vert.friends:
				if next.used == False:
					q.append(next)
					next.used = True
		for node in self.nodes:
			if node.used == False:
				ans = False
				break

		for node in self.nodes: #возращаем исходные значения для следующего обхода
			node.used = False

		return ans

	def set_node_coords(self, node, x, y):
		node.coords[0] = x
		node.coords[1] = y

	#physics
	def apply_force(self):  # be careful, forces must be set to zero somewhere!!!
		for pair in combinations(self.nodes, 2):
			fst = pair[0]
			scnd = pair[1]
			dist = ((fst.coords[0] - scnd.coords[0]) ** 2 + (fst.coords[1] - scnd.coords[1]) ** 2) ** 0.5
			if (dist != 0):
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

	def load_graph(self):
		file = open('members.txt', 'r')
		for line in file:
			line = line.strip()
			arr = line.split()
			id = arr[0]
			if arr[1:] != []:
				node = Node.id_to_node(int(id))
				if node == None:
					node = self.add_node(int(id))
				for friend_id in arr[1:]:
					friend = Node.id_to_node(int(friend_id))
					if friend == None:
						friend = self.add_node(int(friend_id))
					self.add_edge(node, friend)
		print('ok')
		print('nodes at all: ' + str(self.node_cnt))

	def set_groups(self):
		for el in self.nodes:
			self.groups.add(el)

if __name__ == '__main__':
	g = Graph()
	is_connected = g.go_in_width(Node.id_to_node(6))
	print('граф связен: '+str(is_connected))


