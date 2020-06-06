
from graph import Graph
from node import Node
g = Graph()
print('''
sintaxis:
add_e id1 id2
del_e id1 id2
friends id
del_n id
setcoord id x y
''')
while True:
	inp = input('>')
	if inp == "q":
		break
	if inp == "c":
		print(g.is_connected) #TODO - write is_connected based on breadth first search for the debug purposes
		pass
	else:
		commands = inp.split()
		if commands[0] == "add_e":
			if Node.id_node_dict.get(commands[1]) == None:
				g.add_node(commands[1])
			if Node.id_node_dict.get(commands[2]) == None:
				g.add_node(commands[2])
			fst, scnd = Node.id_to_node(commands[1]), Node.id_to_node(commands[2])
			g.add_edge(fst, scnd)
		if commands[0] == "del_e":
			fst, scnd = Node.id_to_node(commands[1]), Node.id_to_node(commands[2])
			g.del_edge(fst, scnd)
		if commands[0] == "friends":
			print(Node.id_to_node(commands[1]).friends)
		if commands[0] == "print":
			for node in g.nodes:
				s = node.id + ' ' + str([friend.id for friend in node.friends])
				print(s, node.coords)
		if commands[0] == 'del_n':
			g.del_node(Node.id_to_node(commands[1]))
		if commands[0] == 'setcoord':
			g.set_node_coords(Node.id_to_node(commands[1]),commands[2],commands[3])
