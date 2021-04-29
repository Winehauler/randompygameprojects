import pygame
from pygame.locals import *


from importlib import reload

import Map
reload(Map)

import Jibbles
reload(Jibbles)

import Graphics
reload(Graphics)

import Constants
reload(Constants)
from Constants import *



resolution = (1200, 800)
FPS = 60


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(resolution)
    running = 1
    frame = 0

    m = Map.Map((resolution[0]//TILESIZE, resolution[1]//TILESIZE))
    j = Jibbles.Jibbles(m.elevation)
    renderer = Graphics.Renderer(screen)

    
    while running:
        frame += 1
        for event in pygame.event.get():
            if event.type == QUIT:
                running = 0
            elif event.type == KEYDOWN:
                if event.key == 27:  # esc
                    running = 0
            elif event.type == KEYUP:
                pass
            else:
                pass
                #print(event)
        
        screen.fill((0,0,0))
        renderer.render(m)
        j.tick()
        renderer.render(j)

        pygame.display.flip()
        clock.tick(FPS)
        pygame.display.set_caption("FPS: {}".format(clock.get_fps()))
    pygame.quit()
