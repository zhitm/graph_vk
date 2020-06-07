from graph import Graph
from node import Node
from additional_graph_methods import make_subset
g = Graph()
g.load_graph('members.txt')
component_nodes = []
component_file = open('component0.txt', 'r')
for line in component_file:
	line.strip()
	component_nodes.append(Node.id_to_node(line))
g = make_subset(g, component_nodes)

def find_dQ(node, node_dest, M):
	sum_in = g.loop_cnt(node_dest)
	k_iin = g.weight_cnt(node, node_dest)
	sum_tot = g.weight_with_outside_cnt(node_dest)
	k_i = g.loop_cnt(node) + g.weight_with_outside_cnt(node)

	dQ = ( (sum_in + 2*k_iin)/(2*M) -((sum_tot + k_i)/(2*M))**2) - (sum_in/(2*M) - (sum_tot/(2*M))**2 - (k_i/(2*M))**2)

	return dQ

def louavain()
	M = 0
	for node in g.nodes:
		M += len(node.friends)
	M = M / 2

	for node in g.nodes:
		k = len(node.friends)
		g.Q = -0.25 * 1 / (M ** 2) * k ** 2
	while True:
		changed = False
		for node in g.groups:
			for n in node.eaten_nodes:
				for node_dest








		if changed == False:
			break
