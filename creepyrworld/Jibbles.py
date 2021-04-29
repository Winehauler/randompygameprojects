import numpy as np


def diffuse(a, diff):
    kernel = np.array([[1.0,2.0,1.0], [2.0,4.0,2.0], [1.0,2.0,1.0]])
    kernel = kernel / np.sum(kernel)
    kernel *= diff
    arraylist = []
    for y in range(3):
        temparray = np.copy(a)
        temparray = np.roll(temparray, y - 1, axis=0)
        for x in range(3):
            temparray_X = np.copy(temparray)
            temparray_X = np.roll(temparray_X, x - 1, axis=1)*kernel[y,x]
            arraylist.append(temparray_X)

    arraylist = np.array(arraylist)
    arraylist_sum = np.sum(arraylist, axis=0)
    return arraylist_sum



class Jibbles:
    def __init__(self, elevation_map):
        shape = elevation_map.shape
        
        self.elevation = elevation_map
        #self.sources = [((shape[0]//2, shape[1]//2), 16)]
        self.sources = []
        self.sources.append(((shape[0]//3, shape[1]//3), 32))
        self.sources.append(((shape[0]//3, 2*shape[1]//3), 128))
        self.heights = np.zeros(self.elevation.shape)
        self.diffusion = 1/5
        self.floor_height = 160

        self.offset_directions = [(i, j) for i in range(-1, 2) \
                                         for j in range(-1, 2)
                                  if not abs(i + j) in [0, 2]]

        

    def get_height(self, x, y):
        return self.elevation[x, y] * self.floor_height + self.heights[x, y]


    def _diffuse1(self, x, y):
        height = self.get_height(x, y)
        if self.heights[x, y] == 0:
            return
        total_drain = 0
        adj = []
        np.random.shuffle(self.offset_directions)
        for offsetx, offsety in self.offset_directions:
            xx = x+offsetx
            yy = y+offsety
            h = self.get_height(xx, yy)
            if h < height:
                total_drain += height - h
                adj.append((xx, yy, h))

        for xx, yy, h in adj:
            self.heights[xx, yy] += self.heights[x, y] // (len(adj)+1)
            self.heights[x, y] -= self.heights[x, y] // (len(adj)+1)
        np.clip(self.heights, 0, self.floor_height*self.elevation.max())


    def diffuse(self):
        for x in range(1, self.heights.shape[0]-1):
            for y in range(1, self.heights.shape[1]-1):
                if self.heights[x, y] == 0:
                    continue
                self._diffuse1(x, y)


    def tick(self):
        for (x, y), strength in self.sources:
            self.heights[x, y] += strength
        #self.heights = blur(self.heights, self.diffusion)
        self.diffuse()


    def accept_render(self, renderer):
        renderer.render_jibbles(self)
    
