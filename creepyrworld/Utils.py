import pygame
import numpy as np


Vector = pygame.Vector2

def vec2int(v):
    return [int(x) for x in v]


randint = np.random.randint


def scale(surface, shape, keep_ratio=False, fix_shape=False, bg_fill=None):
    '''
    if :fix_shape: is False and :keep_ratio: is True create Surface(:shape:) and center scaled surface
    bg_fill=COLOR   fill with COLOR, has no effect if :fix_shape: is True
    '''
    
    if keep_ratio is False:
        return pygame.transform.scale(surface, shape)


    def scale(w, h, x, y):
        nw = y * w / h
        nh = x * h / w
        if not nw >= x:
            return nw or 1, y
        return x, nh or 1

    _shape = scale(surface.get_width(), surface.get_height(),
                   shape[0], shape[1])
    _shape = [int(s) for s in _shape]
    
    if fix_shape:
        return pygame.transform.scale(surface, _shape)

    scaled_surface = pygame.Surface(shape, flags=SRCALPHA)
    if bg_fill is not None:
        scaled_surface.fill(bg_fill)

    max_i = shape.index(max(shape))
    offset = shape[max_i] // 2 - _shape[max_i] // 2
    tl = [0, 0]
    tl[max_i] = offset

    scaled_surface.blit(pygame.transform.scale(surface, _shape), tl)
    return scaled_surface
