import random
from mathutils import *

from PIL import Image

#---PERLIN NOISE---
class PerlinNoise:
    def __init__(self, seed:int):
        self.seed = seed

    def evaluate(self, x:float, y:float)->float:
        sample_point = Vector(x,y)
        
        int_x = int(x)
        int_y = int(y)

        # Lattice Grid corners
        # g4----g3
        # |      |
        # |      |
        # g1----g2
        g1 = Vector(int_x, int_y)
        g2 = Vector(int_x + 1, int_y)
        g3 = Vector(int_x + 1, int_y + 1)
        g4 = Vector(int_x, int_y + 1)

        # Displacement Vectors
        d1 = sample_point - g1
        d2 = sample_point - g2
        d3 = sample_point - g3
        d4 = sample_point - g4

        # Seed with random gradient vectors
        # rg4----rg3
        # |      |
        # |      |
        # rg1----rg2
        rg1 = self.getRandVector(int(g1.x), int(g1.y))
        rg2 = self.getRandVector(int(g2.x), int(g2.y))
        rg3 = self.getRandVector(int(g3.x), int(g3.y))
        rg4 = self.getRandVector(int(g4.x), int(g4.y))

        # Dot products
        # q4----q3
        # |      |
        # |      |
        # q1----q2
        q1 = d1 * rg1
        q2 = d2 * rg2
        q3 = d3 * rg3
        q4 = d4 * rg4

        # Bilinear Interpolation
        sx = sample_point.x - int_x
        sy = sample_point.y - int_y

        # q4--r2--q3
        # |   |   |
        # |   f   |
        # |   |   |
        # q1--r1--q2
        r1 = cubic_lerp(q1, q2, sx)
        r2 = cubic_lerp(q4, q3, sx)
        
        final = cubic_lerp(r1, r2, sy)
        
        return final * 0.5 + 0.5


    def getRandVector(self, x, y)->Vector:
        random.seed(atan2(cos(x+self.seed), sin(y+self.seed)))

        return Polar(1, random.random() * radians(360))

    
#---END PERLIN NOISE---

# Implementation
def main():
    pn = PerlinNoise(1)

    zoom = 16

    dimx = 512
    dimy = 512

    offset_x = 0
    offset_y = 0


    img = Image.new('L', (dimx, dimy))
    pixels = img.load()

    for y in range(dimy):
        for x in range(dimx):
            n = pn.evaluate(
                (x + offset_x)/zoom,
                (y + offset_y)/zoom
            )

            
            pixels[x, y] = int(n*255)

    img.show()
            

if (__name__ == '__main__'):
    main()