from node import Node
from collections import deque
class Graph:
	def __init__(self):
		self.nodes = []
		self.graph = {}
		self.node_cnt = 0
		self.is_connected = True
	def add_node(self, id):
		node = Node.id_to_node(id)
		self.nodes.append(node)
		self.graph.update({node: node.friends})
		self.node_cnt += 1
		Node.id_node_dict.update({id: node})

	def del_node(self, node):
		if node in self.nodes:
			self.nodes.remove(node)
		for friend in node.friends:
			friend.friends.discard(node)
			self.graph.update({friend: friend.friends})
		self.graph.pop(node)
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


if __name__ == '__main__':
	g = Graph()
	file = open('members.txt', 'r')
	for line in file:
		line = line.strip()
		arr = line.split()
		id = arr[0]
		if arr[1:] != None:
			g.add_node(id)
			node = Node.id_to_node(id)
			for friend_id in arr[1:]:
				node = Node.id_to_node(id)
				friend = Node.id_to_node(friend_id)
				g.add_edge(node, friend)
		else:
			pass
	print('ok')

