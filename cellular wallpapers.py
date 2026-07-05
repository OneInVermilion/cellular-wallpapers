#imports
import cmath
from math import ceil, cos, sin
import numpy as np
from PIL import Image

#   Mandelbrot Set
#   Wolfram 18 (Serpinsky Triangle)
#   Wolfram 30
#   Langtons ant
#Conways life (special seed)
#Spiraling prime numbers diagonal rays
#Spiral (just a spiral in 45 deg rotated square)

width: int = 9600
aspect_ratio = (16, 9)
color_background = (0, 0, 0)
color_main = (255, 0, 0)

height: int = width / aspect_ratio[0] * aspect_ratio[1]

def init_grid(w: int, h: int):
    return np.array([[False for _ in range(int(w))] for _ in range(int(h))])

def in_mandelbrot_set(c: complex, iterations: int = 32, threshold: int = 2):
    z = 0
    counter = 0
    while True:
        z = z ** 2 + c
        if abs(z) > threshold:
            return False
        elif counter > iterations:
            return True
        counter += 1

def mandelbrot_set(w: int, h: int): #MANDELBROT SET
    x_center: int = w / 2
    y_center: int = h / 2
    grid = init_grid(w, h)
    pixel_value = 2 / x_center
    for y in range(int(h)):
        for x in range(int(w)):
            r_value = (x - x_center) * pixel_value
            i_value = (y - y_center) * pixel_value
            z = complex(r_value, i_value)
            ims = in_mandelbrot_set(z)
            grid[y][x] = ims
    return grid

def next_cell(left: bool, mid: bool, right: bool, rule: int):
    rule = "{0:08b}".format(rule)
    def form(cell: bool):
        if cell: return "1"
        return "0"
    state = 7 - int(form(left) + form(mid) + form(right), 2)
    if rule[state] == "1": return True
    return False

def next_gen(grid, rule: int):
    grid_next = np.array([False for _ in range(len(grid))])
    for i in range(len(grid) - 1):
        grid_next[i] = next_cell(grid[i-1], grid[i], grid[i+1], rule)
    grid_next[len(grid) - 1] = next_cell(grid[-2], grid[-1], grid[0], rule)
    return grid_next

def wolfram(w: int, h: int, rule: int): #WOLFRAM
    grid = init_grid(w, h)
    grid[0][int(w / 2)] = True
    for y in range(1, int(h)):
        grid[y] = next_gen(grid[y - 1], rule)
    return grid

def langtonsant(w: int, h: int): #LANGTON'S ANT
    grid = init_grid(w, h)
    x: int = w / 2
    y: int = h / 2
    rotation = 0
    while True:
        if x <= 0 or x >= w or y <= 0 or y >= h: break
        grid[int(y)][int(x)] = not grid[int(y)][int(x)]
        if grid[int(y)][int(x)]: rotation += 90
        else: rotation -= 90
        rotation = rotation % 360
        match rotation:
            case 270: y += 1
            case 0: x -= 1
            case 90: y -= 1
            case 180: x += 1
    return grid

def img_gen(grid, name: str):
    w = len(grid[0])
    h = len(grid)
    img = Image.new(mode="RGB", size=(w, h), color=color_background)
    pixels = img.load()
    for y in range(h):
        for x in range(w):
            if grid[y][x] == True: pixels[x, y] = color_main
    img.save(name + ".png")

#img_gen(mandelbrot_set(width, height), "mandelbrot_set_test")
img_gen(wolfram(width, height, 30), "rule30_small 16-9 TEST")
#img_gen(wolfram(width, height, 18), "serpinsky_triangle")
#img_gen(langtonsant(width/10, height/10), "langtons_ant")
#img_gen(mandelbrot_set(1920, 1080), "mandelbrot_screen")
