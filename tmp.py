import pygame
import numpy
import random
import time
from node import Node
from view import View
from graph import Graph
from itertools import combinations
from additional_graph_methods import make_subset
from threading import Thread
pygame.init()
SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 900

g = Graph()
g.load_graph('members.txt')
component_nodes = []
component_file = open('component0.txt', 'r')
for line in component_file:
	line.strip()
	component_nodes.append(Node.id_to_node(line))

component = make_subset(g, component_nodes)

for node in component.nodes:
	node.coords = numpy.array([random.randint(-200, 200) * 100, random.randint(-100, 100) * 100], dtype=numpy.float64)

for node in component.nodes:
	s = str(node.id) + ' ' + str([friend.id for friend in node.friends])
	print(s, node.coords)



for node in g.nodes:
	node.coords = numpy.array([random.randint(-200, 200) * 100, random.randint(-100, 100) * 100], dtype=numpy.float64)

pairs = [i for i in combinations(component.nodes, 2)]

while True:
	start_time = time.time()

	threads_cnt = 4
	threads = []
	# pair_array = [x for x in pairs]
	pair_array = pairs
	cnt_comp = len(pair_array)
	for i in range(threads_cnt - 1):
		array = pair_array[:cnt_comp // threads_cnt]
		pair_array = pair_array[cnt_comp // threads_cnt:]
		th = Thread(target=component.apply_force, args=(array,))
		th.start()
		threads.append(th)
	# component.apply_force(array)
	th = Thread(target=component.apply_force, args=(pair_array,))
	th.start()
	threads.append(th)

	# component.apply_force(pair_array)

	for thr in threads:
		thr.join()


	print(time.time() - start_time)