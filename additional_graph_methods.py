import copy

def make_subset(g, node_set): #выделяет подграф по маске node_set
	g_copy = copy.copy(g)
	g_nodes_list = list(g_copy.nodes)

	for node in g_nodes_list:
		if node not in node_set:
			g_copy.del_node(node)
		else:
			pass
	return g_copy
