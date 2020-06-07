import copy
def validate(g):
	g_copy = copy.copy(g)
	for node in g_copy.nodes:
		if len(node.friends) > 0:
			friends_list = list(node.friends)
			for friend in friends_list:
				try:
					node.friends.remove(friend)
					friend.friends.remove(node)
				except:
					print("invalid")
					return False
				g.graph.update({node: node.friends})
				g.graph.update({friend: friend.friends})

	for node in g_copy.nodes:
		if len(node.friends) > 0:
			print("invalid")
			return False
	print("valid")
	return True


def make_subset(g, node_set):
	g_copy = copy.copy(g)
	g_nodes_list = list(g_copy.nodes)

	for node in g_nodes_list:
		if node not in node_set:
			g_copy.del_node(node)
		else:
			pass #maybe an error? i don't know
	return g_copy

def cache_edges(g): # before drawing
	g.has_valid_cache = True
	edges = set()
