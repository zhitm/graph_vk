from graph import Graph
from node import Node
g = Graph()
while True:
	inp = input('>')
	if inp == "q":
		break
	if inp == "c":
		print(g.is_connected) #TODO - write is_connected based on breadth first search for the debug purposes
		pass
	else:
		commands = inp.split()
		if commands[0] == "add":
			g.add_node(commands[1])
			g.add_node(commands[2])
			fst, scnd = Node.id_to_node(commands[1]), Node.id_to_node(commands[2])
			g.add_edge(fst, scnd)
		if commands[0] == "del":
			fst, scnd = Node.id_to_node(commands[1]), Node.id_to_node(commands[2])
			g.del_edge(fst, scnd)
		if commands[0] == "friends":
			print(Node.id_to_node(commands[1]).friends)
		if commands[0] == print:
			for node in g.nodes:
				print(node.id, " ", node.friends)

