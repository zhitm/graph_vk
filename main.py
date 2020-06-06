import pygame
import numpy
import random
from node import Node
from view import View
from graph import Graph
from itertools import combinations

pygame.init()
SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 900
"""
g = Graph()
n0 = g.add_node(0)
n1 = g.add_node(1)
n2 = g.add_node(2)

g.add_edge(n0, n1)
g.add_edge(n1, n2)
g.add_edge(n0, n2)

Node.set_node_coords(n0, 50, 50)
Node.set_node_coords(n1, -50, -50)
Node.set_node_coords(n2, 50, -50)
"""

g = Graph()
N = 200
p = 20 / 200
for pair in combinations(range(0, N), 2):
    if random.random() < p:
        n1 = g.add_node(str(pair[0]))
        n2 = g.add_node(str(pair[1]))
        g.add_edge(n1, n2)
for node in g.nodes:
    node.coords = numpy.array([random.randint(-200, 200) * 100, random.randint(-100, 100) * 100], dtype=numpy.float64)

for node in g.nodes:
    s = node.id + ' ' + str([friend.id for friend in node.friends])
    print(s, node.coords)

view = View(-400 * 100, 200 * 100, SCREEN_WIDTH, SCREEN_HEIGHT, 800 * 100)

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
running = True

#state variables
mouse_pressed = False
mouse_pos = numpy.array([0,0])
click_pos = numpy.array([0,0])
origin_before_click = ([0, 0])
scroll_multiplier = 1
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pressed = True
            origin_before_click = view.v_tl
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


    screen.fill((255, 255, 255))
    g.draw(view, pygame, screen)
    g.apply_force()
    g.move(0.01)

    pygame.display.flip()

pygame.quit()