import numpy
import random
import time
from node import Node
from view import View
from graph import Graph
from itertools import combinations
from additional_graph_methods import make_subset
import concurrent.futures


def main():
	while True:
		start_time = time.time()
		threads_cnt = 12
		pair_array = pairs
		cnt_comp = len(pair_array)
		arr_of_arrs = []
		for i in range(threads_cnt - 1):
			array = pair_array[:cnt_comp // threads_cnt]
			arr_of_arrs.append(array)
			pair_array = pair_array[cnt_comp // threads_cnt:]
		arr_of_arrs.append(pair_array)

		with concurrent.futures.ProcessPoolExecutor(max_workers=threads_cnt) as executor:
			for _ in executor.map(component.apply_force, arr_of_arrs):
				pass

		print(time.time() - start_time)

		g.move()


if __name__ == '__main__':

	g = Graph()
	g.load_graph('members.txt')
	component_nodes = []
	component_file = open('component0.txt', 'r')
	for line in component_file:
		line.strip()
		component_nodes.append(Node.id_to_node(line))

	component = make_subset(g, component_nodes)

	for node in component.nodes:
		node.coords = numpy.array([random.randint(-200, 200) * 100, random.randint(-100, 100) * 100],
								  dtype=numpy.float64)

	for node in component.nodes:
		s = str(node.id) + ' ' + str([friend.id for friend in node.friends])
		print(s, node.coords)

	for node in g.nodes:
		node.coords = numpy.array([random.randint(-200, 200) * 100, random.randint(-100, 100) * 100],
								  dtype=numpy.float64)

	pairs = [i for i in combinations(component.nodes, 2)]

	main()

