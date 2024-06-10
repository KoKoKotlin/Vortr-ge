import pygame
import time

import numpy as np
from scipy.interpolate import splrep, splev, CubicSpline
from math import sin, pi

WHITE = (255,255,255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WIDTH = 1000.0
HEIGHT = 1000.0

WORLD_WIDTH = 10.0
WORLD_HEIGHT = 10.0

def lerp(x, y, t):
    return (1 - t) * x + t * y

def create_spline(start, p1, p2, end):
    spline = lambda t: (lerp(lerp(start[0], p1[0], t), lerp(p1[0], end[0], t), t), lerp(lerp(start[1], p1[1], t), lerp(p1[1], end[1], t), t))
    return spline

def world_to_screen(world_coord):
    screen_x = world_coord[0] / WORLD_WIDTH * WIDTH + WIDTH / 2
    screen_y = world_coord[1] / WORLD_HEIGHT * HEIGHT - HEIGHT / 2
    
    return (screen_x, -screen_y)

def render_curve(curve, samples, color, window):
    values = np.arange(0, 1, 1/samples)

    results = [curve(v) for v in values]
    for coord in results:
        pygame.draw.circle(window, color, world_to_screen(coord), 1.5)

def render_homotopy(curve1, curve2, t, samples, window):
    values = np.arange(0, 1, 1/samples)

    results = [(1-t) * np.array(curve1(v)) + t * np.array(curve2(v)) for v in values]
    for coord in results:
        pygame.draw.circle(window, WHITE, world_to_screen(coord), 1.5)

def calc_t(t):
    t = t % 2.0
    return t if t < 1 else 2 - t

def main():
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Homotopie-Demo")
    
    pygame.font.init() 
    font = pygame.font.SysFont('monospace', 30)
    
    t = 0
    while True:
        window.fill((51,51,51))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit(0)
        
        p1 = [-4, -1]
        p2 = [4, 2]
        curve1 = create_spline(p1, [2, 5], None, p2)
        curve2 = create_spline(p1, [-1, -6], None, p2)
        render_curve(curve1, 2000, GREEN, window)
        render_curve(curve2, 2000, BLUE, window)
        render_homotopy(curve1, curve2, calc_t(t), 2000, window)
        pygame.draw.circle(window, BLACK, world_to_screen(p1), 5)
        pygame.draw.circle(window, BLACK, world_to_screen(p2), 5)
        
        text_surface = font.render(f"t = {round(calc_t(t), 2)}", True, WHITE)
        window.blit(text_surface, (0, 0))

        pygame.display.flip()
        time.sleep(0.001)
        t = t + 0.001 * 7

if __name__ == "__main__":
    main()