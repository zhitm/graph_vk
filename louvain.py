from graph import Graph
from node import Node
from additional_graph_methods import make_subset
g = Graph()
g.load_graph('members_test.txt')
component_nodes = []
component_file = open('component.txt', 'r')
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

def new_friends_format(nodes):
	for node in nodes:
		for friend in node.friends:
			node.friends_lv.update({friend: 1})

def loop_cnt(node):
	if node.friends_lv.get(node) == None:
		return 0
	else:
		return node.friends_lv.get(node)

def k_iin_f(node, group):
	mass = 0
	for friend in node.friends_lv:
		if friend in group:
			mass += node.friends_lv.get(friend)
	return mass

def sum_tot_f(node):
	mass = 0
	for friend in node.friends_lv:
		if friend not in node.eaten_ids:
			mass += node.friends_lv.get(friend)
	return mass



def find_dQ(node, group):
	sum_in = int(loop_cnt(node)) #+
	k_iin = int(k_iin_f(node, group)) #+
	sum_tot = int(sum_tot_f(node)) #+
	k_i = int(loop_cnt(node)) + int(sum_tot_f(node)) #+

	dQ = ( (sum_in + 2*k_iin)/(2*M) -((sum_tot + k_i)/(2*M))**2) - (sum_in/(2*M) - (sum_tot/(2*M))**2 - (k_i/(2*M))**2)

	return dQ

'''lion's code'''
nodes = set()
for el in g.nodes:
	nodes.add(el)



groups = []


def louvain():
	reset_groups()
	new_friends_format(nodes)
	cnt = 0
	while True:
		mozhem = True
		while mozhem:
			cnt+=1
			print(cnt)
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
		print('ok')
		break


def merge_groups():  # DONE
	for group in groups:
		merge_group(group)


def merge_group(group):  # DONE
	if len(group) == 0:
		groups.remove(group)
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
	for friend, mass in node_1.friends_lv:
		new_node.friends_lv.update({friend: mass})

	for friend, mass in node_2.friends_lv:
		if friend not in new_node.friends_lv.keys:
			new_node.friends_lv.update({friend: mass})
		else:
			mass1 = new_node.friends_lv.get(friend)
			new_node.friends_lv.update({friend: mass + mass1})

	for friend in new_node.friends_lv:
		mass = new_node.friends_lv.get(friend)
		friend.friends_lv.update({new_node: mass})

	new_node.eaten_ids = node_1.eaten_ids + node_2.eaten_ids
	nodes.add(new_node)
	nodes.discard(node_1)
	nodes.discard(node_2)
	return new_node


def reset_groups():  # DONE
	groups.clear()
	for node in nodes:

		node.current_group = set()
		node.current_group.add(node)
		groups.append(node.current_group)


def move_to(node, group):  # DONE
	if len(node.current_group) == 1:
		groups.remove(node.current_group)
	node.current_group.discard(node)
	group.add(node)


louvain()