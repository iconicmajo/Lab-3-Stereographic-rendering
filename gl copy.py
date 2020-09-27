#Maria Jose Castro Lemus 
#181202
#Graficas por Computadora - 10
#RT2: Teddys
#snowman

import struct 
from materials import coal, snow, ivory, carrot,white,red
from sphere import Sphere
from mathfunc import norm, V3, color, char,dword, word, sub, length, dot, mul,reflect
from collections import namedtuple
import random
from numpy import matrix, cos, sin, tan, pi
import math
from light import Light

BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)

class Render(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.scene = []
        self.activeTexture = WHITE
        self.clear()

    def clear(self):
        self.framebuffer= [
        [self.activeTexture for x in range(self.width)]
        for y in range(self.height)
        ]

    def point(self, x, y, selectColor=None):
        try:
            self.framebuffer[y][x] = self.activeTexture
        except:
            pass
        
    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        #r = Render(width,height)

    def write(self, filename):
        f = open(filename, 'bw')
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        #image header 
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        #pixel data
        for x in range(self.width):
            for y in range(self.height):
                f.write(self.framebuffer[y][x].toBytes())
        f.close()

        #Referencia del repositorio ejemplo de dennis
    def glFinish(self, filename='Spheres.bmp'):
        self.write(filename)

    def scene_intersect(self, orig, direction):
        zbuffer = float('inf')
        
        material = None
        intersect = None
        
        for obj in self.scene:
            hit = obj.ray_intersect(orig, direction)
            if hit is not None:
                if hit.distance < zbuffer:
                    zbuffer = hit.distance
                    material = obj.material
                    intersect = hit
        return material, intersect

        '''for obj in self.scene:
            if obj.ray_intersect(orig, direction):
                return obj.material
        return None'''

    def cast_ray(self, orig, direction):
        material, intersect = self.scene_intersect(orig, direction)

        if material is None:
            return self.activeTexture

        light_dir = norm(sub(self.light.position, intersect.point))
        light_distance = length(sub(self.light.position, intersect.point))

        offset_normal = mul(intersect.normal, 1.1)  # avoids intercept with itself
        shadow_orig = sub(intersect.point, offset_normal) if dot(light_dir, intersect.normal) < 0 else sub(intersect.point, offset_normal)
        shadow_material, shadow_intersect = self.scene_intersect(shadow_orig, light_dir)
        shadow_intensity = 0

        if shadow_material and length(sub(shadow_intersect.point, shadow_orig)) < light_distance:
            shadow_intensity = 0.9

        intensity = self.light.intensity * max(0, dot(light_dir, intersect.normal)) * (1 - shadow_intensity)

        reflection = reflect(light_dir, intersect.normal)
        specular_intensity = self.light.intensity * (
        max(0, -dot(reflection, direction))**material.spec
        )

        diffuse = material.diffuse * intensity * material.albedo[0]
        specular = color(255, 255, 255) * specular_intensity * material.albedo[1]
        return diffuse + specular

        
        

    def render(self):
        fov = int(pi/2)
        for y in range(self.height):
            for x in range(self.width):
                i =  (2*(x + 0.5)/self.width - 1) * tan(fov/2) * self.width/self.height
                j =  (2*(y + 0.5)/self.height - 1) * tan(fov/2)
                direction = norm(V3(i, j, -1))
                self.framebuffer[y][x] = self.cast_ray(V3(0,0,0), direction)
                


r = Render(1000, 1000)
r.light = Light(
    position = V3(0, 0, 20),
    intensity = 1.5
)
r.scene = [
    #snowballs
    Sphere(V3(3.3,0,-10), 1.5, red),
    Sphere(V3(-3.3,0,-10), 1.5, red)
]
r.render()
r.glFinish()
