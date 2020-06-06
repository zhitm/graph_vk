import pygame
import numpy
from node import Node
from view import View

pygame.init()
SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 900

node = Node(0)
view = View(-2, 1, SCREEN_WIDTH, SCREEN_HEIGHT, 4)

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
running = True

#state variables
mouse_pressed = False
mouse_pos = numpy.array([0,0])
click_pos = numpy.array([0,0])
origin_before_click = ([0, 0])
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pressed = True
            origin_before_click = view.v_tl
            click_pos = numpy.array(pygame.mouse.get_pos())

        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pressed = False

        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = numpy.array(pygame.mouse.get_pos())

    if mouse_pressed:
        new_origin = origin_before_click - numpy.array(
            view.antitransform((mouse_pos)[0], (mouse_pos)[1])) + numpy.array(
            view.antitransform(click_pos[0], click_pos[1]))
        view.set_v_tl(new_origin)



    screen.fill((255, 255, 255))
    node.draw(view, pygame, screen)

    pygame.display.flip()

pygame.quit()