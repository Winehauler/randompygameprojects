import numpy as np
import pygame
from pygame.locals import *


import Utils

from Constants import *


MAP_ELEVATION_COLORS = {
    0: (29, 40, 52),
    1: (46, 40, 32),
    2: (58, 44, 24),
    3: (40, 68, 27),
    4: (24, 47, 14),
    5: (61, 61, 61),
    6: (72, 86, 85),
    }



class Renderer:


    def __init__(self, screen):
        self.screen = screen
        self.cache = {}
    

    def render(self, obj):
        obj.accept_render(self)


    def render_jibbles(self, jibbles):
        alpha1 = 150
        alpha2 = 255
        color0 = pygame.Color((0,0,0,0))
        color1 = np.array((90, 65, 150, alpha1))
        color2 = np.array((100, 24, 95, alpha2))
        max_value = (jibbles.elevation.max()-2) * jibbles.floor_height

        def getcolor(v):
            if v == 0:
                return color0
            vn = float(v) / max_value
            color = color1 * (1 - vn) + color2 * vn
            if vn >= 1:
                color = [255, 0, 255]
            np.clip(color, 0, 255)
            return Utils.vec2int(color)

        jibbles_surface = pygame.Surface(jibbles.elevation.shape, flags=SRCALPHA)
        pix_arr = pygame.PixelArray(jibbles_surface)
        for x in range(jibbles_surface.get_width()):
            for y in range(jibbles_surface.get_height()):
                color = getcolor(jibbles.heights[x,y])
                if sum(color) > 0:
                    try:
                        pix_arr[x][y] = pygame.Color(color)
                    except ValueError:
                        print("Invalid Color: {}".format(color))
        del pix_arr
        target_size = pygame.Vector2(jibbles.heights.shape) * TILESIZE
        jibbles_surface = Utils.scale(jibbles_surface, Utils.vec2int(target_size))

        self.screen.blit(jibbles_surface, (0,0))

        for position, strength in jibbles.sources:
            position = [int(p*TILESIZE+TILESIZE//2) for p in position]
            pygame.draw.circle(self.screen, [200, 100, 100], position, TILESIZE//2)


    def _render_jibbles_heightmap(self, jibbles):
        heights = jibbles.heights
        colormap = np.zeros(list(heights.shape) + [3])
        
        
        alpha1 = 150
        alpha2 = 255
        color0 = pygame.Color((0,0,0,0))
        color1 = np.array((100, 65, 120, alpha1))
        color2 = np.array((100, 24, 23, alpha2))
        max_value = (jibbles.elevation.max()-2) * jibbles.floor_height

        def getcolorR(v):
            if v == 0:
                return color0
            vn = float(v) / max_value
            color = color1 * (1 - vn) + color2 * vn
            if vn >= 1:
                color = [255, 0, 255]
            np.clip(color, 0, 255)
            return color[0]

        def getcolorG(v):
            if v == 0:
                return color0
            vn = float(v) / max_value
            color = color1 * (1 - vn) + color2 * vn
            if vn >= 1:
                color = [255, 0, 255]
            np.clip(color, 0, 255)
            return color[1]

        def getcolorB(v):
            if v == 0:
                return color0
            vn = float(v) / max_value
            color = color1 * (1 - vn) + color2 * vn
            if vn >= 1:
                color = [255, 0, 255]
            np.clip(color, 0, 255)
            return color[2]

        getcolors = [getcolorR, getcolorG, getcolorB]
        getcolors = [np.vectorize(gc_func) for gc_func in getcolors]
        for c in range(3):
            colormap[:,:,c] = getcolors[c](heights)
        surface = pygame.surfarray.make_surface(colormap)
        surface.set_colorkey((0,0,0))
        return surface


    def render_jibbles(self, jibbles):
        surface = self._render_jibbles_heightmap(jibbles)
        target_size = pygame.Vector2(jibbles.heights.shape) * TILESIZE
        surface = Utils.scale(surface, Utils.vec2int(target_size))

        self.screen.blit(surface, (0,0))

        for position, strength in jibbles.sources:
            position = [int(p*TILESIZE+TILESIZE//2) for p in position]
            pygame.draw.circle(self.screen, [200, 100, 100], position, TILESIZE//2)


    def render_map(self, map):
        cache = self.cache
        if map in cache:
            self.screen.blit(cache[map], (0,0))
            return

        map_surface = pygame.Surface(map.elevation.shape)
        pix_arr = pygame.PixelArray(map_surface)
        for x in range(map_surface.get_width()):
            for y in range(map_surface.get_height()):
                color = MAP_ELEVATION_COLORS[map.elevation[x,y]]
                pix_arr[x][y] = pygame.Color(color)
        del pix_arr
        target_size = pygame.Vector2(map.elevation.shape) * TILESIZE
        map_surface = Utils.scale(map_surface, Utils.vec2int(target_size))
        cache[map] = map_surface
        self.screen.blit(cache[map], (0,0))

        
        
