from graph import Graph
from node import Node
from additional_graph_methods import make_subset
from itertools import combinations
g = Graph()
g.load_graph('members.txt')
component_nodes = []
component_file = open('component0.txt', 'r')
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
		node.friends_lv.update({node: 0})
		for friend in node.friends:
			node.friends_lv.update({friend: 1})

def loop_cnt(node):
	return node.friends_lv[node]

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

def weighted_degree(node):
	return node.degree


def group_Q(group):
	Q = 0
	pairs = combinations(group, 2)
	for pair in pairs:
		node1 = pair[0]
		node2 = pair[1]
		Q += node1.friends_lv[node2]
		Q -= sum(friend.friends_lv[node1] for friend in node1.friends_lv) * sum(
			friend.friends_lv[node2] for friend in node2.friends_lv) / (2 * M)
	for node in group:
		Q += node.friends_lv[node]
		wgt_degree = weighted_degree(node)
		Q -= wgt_degree*wgt_degree / (2*M)
	return Q / (2 * M)


def find_dQ(node, group):
	if node in group:
		return 0

	dQ = 0
	for same_group_node in node.current_group:
		if same_group_node == node:
			pass
		else:
			dQ -= (node.friends_lv[same_group_node] - node.degree * same_group_node.degree / (2 * M)) / (2 * M)

	for other_group_node in group:
		dQ += (node.friends_lv[other_group_node] - node.degree * other_group_node.degree / (2 * M)) / (2 * M)

	return dQ


'''lion's code'''
nodes = set()
for el in g.nodes:
	nodes.add(el)



groups = []


def louvain(g, groups):
	for node in g.nodes:
		node.cnt_degree()
	reset_groups()
	new_friends_format(g.nodes)
	cnt = 0
	while True:
		mozhem = True
		while mozhem:
			cnt+=1
			print(cnt)
			mozhem = False
			sub_cnt = 0
			for node in g.nodes:
				print(sub_cnt)
				sub_cnt += 1
				friends_groups = [friend.current_group for friend in node.friends]

				max_dQ = -10
				max_group = None
				for group in friends_groups:
					leng = len(group)
					new_dQ = find_dQ(node, group)
					if new_dQ > max_dQ:
						max_group = group
						max_dQ = new_dQ


				if max_group is None:
					print("no best option")
					continue

				possible_dQ = find_dQ(node, max_group)
				if possible_dQ != max_dQ:
					print("Jeez")
				if possible_dQ <= 0.0000001:
					pass
				else:
					g.Q += possible_dQ
					move_to(node, max_group)
					mozhem = True

		outp = open('final.txt', 'w')
		print("Groups:", len(groups), "; their sizes:")
		for group in groups:
			print(len(group))
			for node in group:
				outp.write(str(node.id))
				outp.write('\n')
			outp.write('\n')
			outp.write('\n')
			outp.write('\n')
		outp.close()
		print('ok')
		break


def merge_groups(groups):  # DONE
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
		node_0 = merge_nodes(node_0, node)
	group.clear()
	group.add(node_0)

	return group




def merge_nodes(node_1, node_2):  # DONE
	new_node = Node(Node.cnt*(-1))
	for friend, mass in node_1.friends_lv.items():
		new_node.friends_lv.update({friend: mass})

	for friend, mass in node_2.friends_lv.items():
		if friend not in new_node.friends_lv:
			new_node.friends_lv.update({friend: mass})
		else:
			mass1 = new_node.friends_lv[friend]
			new_node.friends_lv.update({friend: mass + mass1})

	for friend in new_node.friends_lv:
		mass = new_node.friends_lv.get(friend)
		friend.friends_lv.update({new_node: mass})

	new_node.eaten_ids = node_1.eaten_ids | node_2.eaten_ids
	nodes.add(new_node)
	nodes.discard(node_1)
	nodes.discard(node_2)
	return new_node


def reset_groups():  # DONE
	groups.clear()
	for node in g.nodes:

		node.current_group = set()
		node.current_group.add(node)
		groups.append(node.current_group)


def move_to(node, group):  # DONE
	if len(node.current_group) == 1:
		groups.remove(node.current_group)
	node.current_group.discard(node)
	group.add(node)
	node.current_group = group


louvain(g, groups)