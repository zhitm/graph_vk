import pygame
import numpy
import random
from node import Node
from view import View
from graph import Graph
from itertools import combinations
from additional_graph_methods import make_subset
from threading import Thread

"""
Файл для рисования графа, используя физическую модель.
Поддерживает передвигание экрана, масштабирование колесом мышки, получение id по клику ПКМ
Физические взаимодействия распараллелены (небезопасно)
"""

pygame.init()
SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 900

g = Graph()
g.load_graph('components\members.txt')
component_nodes = [] # маска по компоненте связности
component_file = open('components\component5.txt', 'r')
for line in component_file:
	line.strip()
	component_nodes.append(Node.id_to_node(line))

component = make_subset(g, component_nodes)


for node in component.nodes:
	node.coords = numpy.array([random.randint(-200, 200) * 100, random.randint(-100, 100) * 100], dtype=numpy.float64)


view = View(-400 * 100, 200 * 100, SCREEN_WIDTH, SCREEN_HEIGHT, 800 * 100)
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
running = True

#переменные состояния
mouse_pressed = False
mouse_pos = numpy.array([0,0])
click_pos = numpy.array([0,0])
origin_before_click = ([0, 0])
scroll_multiplier = 1
should_get_id =  False

click_cnt = 0
pairs = [i for i in combinations(component.nodes, 2)]
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			mouse_pressed = True
			origin_before_click = view.v_tl
			click_pos = numpy.array(pygame.mouse.get_pos())

		elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
			should_get_id = True
			click_pos = numpy.array(pygame.mouse.get_pos())

		elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
			scroll_multiplier *= 1.1

		elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
			scroll_multiplier /= 1.1

		elif event.type == pygame.MOUSEBUTTONUP:
			mouse_pressed = False

		elif event.type == pygame.MOUSEMOTION:
			mouse_pos = numpy.array(pygame.mouse.get_pos())

	if mouse_pressed:
		new_origin = origin_before_click - numpy.array(
			view.antitransform((mouse_pos)[0], (mouse_pos)[1])) + numpy.array(
			view.antitransform(click_pos[0], click_pos[1]))
		view.set_v_tl(new_origin)


	if(scroll_multiplier != 1):
		view.set_dx(view.dx / scroll_multiplier)
		view.set_v_tl(numpy.array(view.antitransform(mouse_pos[0], mouse_pos[1])) + (view.v_tl - numpy.array(view.antitransform(mouse_pos[0], mouse_pos[1]))) / scroll_multiplier)
		scroll_multiplier = 1

	if should_get_id:
		should_get_id = False
		for node in component.nodes:
			tmp = numpy.array(view.transform(node.coords[0], node.coords[1])) - mouse_pos
			dist = tmp[0]*tmp[0] + tmp[1]*tmp[1]
			if dist < 10:
				print(click_cnt, "<-------------------- https://vk.com/id" + str(node.id))
		click_cnt += 1


	screen.fill((255, 255, 255))
	threads_cnt = 2
	threads = []
	pair_array = pairs
	cnt_comp = len(pair_array)
	for i in range(threads_cnt-1):
		array = pair_array[:cnt_comp//threads_cnt]
		pair_array = pair_array[cnt_comp//threads_cnt:]
		th = Thread(target=component.apply_force, args=(array,))
		th.start()
		threads.append(th)
	th=Thread(target=component.apply_force, args=(pair_array,))
	th.start()
	threads.append(th)

	component.move(0.01)
	component.draw(view, pygame, screen)
	for thr in threads:
		thr.join()

	pygame.display.flip()

pygame.quit()