from graph import Graph
from node import Node
from additional_graph_methods import make_subset
g = Graph()
g.load_graph('members.txt')
component_nodes = []
component_file = open('component5.txt', 'r')
for line in component_file:
	line.strip()
	component_nodes.append(Node.id_to_node(line))
g = make_subset(g, component_nodes)

M = 0
for node in g.nodes:
	M += len(node.friends)
M = M / 2

for node in g.nodes:
	k = len(node.friends)
	g.Q = -0.25 * 1 / (M ** 2) * k ** 2


def loop_cnt(node):
	return node.friends[node]

def k_iin_f(node, group):
	mass = 0
	for friend in node.friends:
		if friend in group:
			mass += node.friends.get(friend)
	return mass

def sum_tot_f(node):
	mass = 0
	for friend in node.friends:
		if friend not in node.eaten_ids:
			mass += node.friends.get(friend)
	return mass



def find_dQ(node, group):
	sum_in = loop_cnt(node) #+
	k_iin = k_iin_f(node, group) #+
	sum_tot = sum_tot_f(node) #+
	k_i = g.loop_cnt(node) + sum_tot_f(node) #+

	dQ = ( (sum_in + 2*k_iin)/(2*M) -((sum_tot + k_i)/(2*M))**2) - (sum_in/(2*M) - (sum_tot/(2*M))**2 - (k_i/(2*M))**2)

	return dQ

'''lion's code'''
nodes = set()
for el in g.nodes:
	nodes.add(el)



groups = set()


def louvain():
	reset_groups()
	while True:
		mozhem = True
		while mozhem:
			mozhem = False
			for node in nodes:

				group = max(groups, key=lambda group: find_dQ(node, group))
				possible_dQ = find_dQ(node, group)
				if possible_dQ < 0:
					pass
				else:
					g.Q += possible_dQ
					move_to(node, group)
					mozhem = True

		g.merge_groups()
		g.reset_groups()
		continue


def merge_groups():  # DONE
	for group in groups:
		merge_group(group)


def merge_group(group):  # DONE
	if len(group) == 0:
		groups.discard(group)
		return None

	if len(group) == 1:
		return group

	node_0 = group.pop()

	for node in group:
		node.pop()
		node_0 = merge_nodes(node_0, node)
	group.add(node_0)

	return group




def merge_nodes(node_1, node_2):  # DONE
	new_node = Node(Node.cnt*(-1))
	for friend, mass in node_1.friends:
		new_node.friends.update({friend: mass})

	for friend, mass in node_2.friends:
		if friend not in new_node.friends.keys:
			new_node.friends.update({friend: mass})
		else:
			mass1 = new_node.friends.get(friend)
			new_node.friends.update({friend: mass + mass1})

	for friend in new_node.friends:
		mass = new_node.friends.get(friend)
		friend.friends.update({new_node: mass})

	new_node.eaten_ids = node_1.eaten_ids + node_2.eaten_ids
	nodes.add(new_node)
	nodes.discard(node_1)
	nodes.discard(node_2)
	return new_node


def reset_groups():  # DONE
	groups.clear()
	for node in nodes:
		node.current_group = set(node)
		groups.add(node.current_group)


def move_to(node, group):  # DONE
	if len(node.current_group) == 1:
		groups.discard(node.current_group)
	node.current_group.discard(node)
	group.add(node)


