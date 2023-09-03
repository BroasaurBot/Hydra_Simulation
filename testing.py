import pygame
import pymunk

FPS = 50

pygame.init()
display = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = 0, -1000

class Ball():
    def __init__(self, x, y, radius):
        self.body = pymunk.Body()
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.elasticity = 1
        self.shape.density = 1
        self.radius = radius
        space.add(self.body, self.shape)
    
    def draw(self):
        pygame.draw.circle(display, (0, 255, 0), convert_coordinates(self.body.position), self.radius)

class Floor():
    def __init__(self, a, b, width):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, a, b, width)
        self.width = width
        self.shape.elasticity = 1
        space.add(self.body, self.shape)
    
    def draw(self):
        pygame.draw.line(display, (0, 0, 0), convert_coordinates(self.shape.a), convert_coordinates(self.shape.b), self.width)

class String():
    def __init__(self, b1, b2):
        self.body1 = b1.body
        if type(b2) == tuple:
            x, y = b2
            self.body2 = pymunk.Body(body_type=pymunk.Body.STATIC)
            self.body2.position = x, y
        else:
            self.body2 = b2.body

        joint = pymunk.DampedSpring(self.body1, self.body2,
                                    anchor_a=(0, 0), anchor_b=(0, 0),
                                    rest_length=50, stiffness=50000, damping=10000)
        space.add(joint)
        
    def draw(self):
        pygame.draw.line(display, (0, 0, 0), convert_coordinates(self.body1.position), convert_coordinates(self.body2.position), 1)


def convert_coordinates(pos):
    x, y = pos
    return int(x), 600 - int(y)

def simulation():
    b1 = Ball(300, 400, 20)
    b2 = Ball(300, 200, 20)

    s1 = String(b1, (300, 550))
    s2 = String(b1, b2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        display.fill((255, 255, 255))
        b1.draw()
        b2.draw()
        s1.draw()
        s2.draw()

        b2.body.apply_force_at_world_point((1000000, 0), (10, 0))
        
        clock.tick(FPS)
        space.step(1/FPS)
        pygame.display.update()

simulation()
pygame.quit()