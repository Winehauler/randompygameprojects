import numpy as np
import pygame

from vec_noise import snoise2



def _generate_random_elevation_map(size, num_elevations, noise_zoom, snoise_kwargs={}):
    noise_zoom = 1/noise_zoom
    m = []
    x, y = 0, 0
    for _ in range(size[0]):
        m.append([])
        for _ in range(size[1]):
            m[-1].append(snoise2(x, y, **snoise_kwargs))
            x += noise_zoom
        x = 0
        y += noise_zoom
    m = np.array(m)
    m -= m.min()
    m /= m.max()
    m *= num_elevations
    m = m.astype(int)
    return m
    


class Map:
    NUM_ELEVATIONS = 6
    def __init__(self, size):
        snoise_kwargs = {
            "octaves": 2,
            "base": np.random.random()*1234
            }
        noise_zoom = 25
        
        self.elevation = _generate_random_elevation_map(
            size, self.NUM_ELEVATIONS,
            noise_zoom,snoise_kwargs=snoise_kwargs)


    def accept_render(self, renderer):
        renderer.render_map(self)


