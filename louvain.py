from graph import Graph
from node import Node
from additional_graph_methods import make_subset
from itertools import combinations

"""
Реализует лувенский алгоритм поиска сообществ (только первую итерацию).
Модулярность - величина, которая показывает, насколько хорошо вершины поделены на общества.
Лувенский алгоритм "жадно" увеличивает модулярность, пытаясь переместить вершину в сообщество своих соседей.
Q - обозначенине модулярности графа. Лежит в промежутке от -1/2 до 1
"""

g = Graph()
g.load_graph('components\members.txt')
component_nodes = []
component_file = open('components\component0.txt', 'r')
for line in component_file:
	line.strip()
	component_nodes.append(Node.id_to_node(line))
g = make_subset(g, component_nodes)


M = 0 # масса всех ребер в графе
for node in g.nodes:
	M += len(node.friends)
M = M / 2


def new_friends_format(nodes): # создает словарь friends_lv для каждой вершины из nodes
	for node in nodes:
		node.friends_lv.update({node: 0})
		for friend in node.friends:
			node.friends_lv.update({friend: 1})



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
		Q -= node.degree*node.degree / (2*M)
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
				max_dQ = -10 #случайное маленькое число
				max_group = None
				for group in friends_groups: #однострочный аналог написанного сложно дебажить
					new_dQ = find_dQ(node, group)
					if new_dQ > max_dQ:
						max_group = group
						max_dQ = new_dQ

				possible_dQ = find_dQ(node, max_group)
				if possible_dQ <= 0.0000001:
					pass
				else:
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

def reset_groups():
	groups.clear()
	for node in g.nodes:

		node.current_group = set()
		node.current_group.add(node)
		groups.append(node.current_group)


def move_to(node, group):
	if len(node.current_group) == 1:
		groups.remove(node.current_group)
	node.current_group.discard(node)
	group.add(node)
	node.current_group = group

louvain(g, groups)