from graph import Graph
from node import Node
g = Graph()
print('''
sintaxis:
add_n id
del_n id
add_e id1 id2
del_e id1 id2
friends id
setcoord id x y
printcoord id''')
while True:
	inp = input('>')
	if inp == "q":
		break
	else:
		commands = inp.split()
		if commands[0] == 'add_n':
			g.add_node(int(commands[1]))

		if commands[0] == 'del_n':
			g.del_node(Node.id_to_node(int(commands[1])))

		if commands[0] == "add_e":
			fst, scnd = Node.id_to_node(int(commands[1])), Node.id_to_node(int(commands[2]))
			g.add_edge(fst, scnd)

		if commands[0] == "del_e":
			fst, scnd = Node.id_to_node(int(commands[1])), Node.id_to_node(int(commands[2]))
			g.del_edge(fst, scnd)

		if commands[0] == "friends":
			print(Node.id_to_node(int(commands[1])).friends)

		if commands[0] == "print":
			for node in g.nodes:
				s = str(node.id) + ' ' + str([friend.id for friend in node.friends])
				print(s, node.coords)

		if commands[0] == 'setcoord':
			Node.set_node_coords(Node.id_to_node(float(commands[1])),float(commands[2]),float(commands[3]))

		if commands[0] == 'printcoord':
			print(str(Node.id_to_node(int(commands[1])).x)+str(Node.id_to_node(int(commands[1])).y)    )


