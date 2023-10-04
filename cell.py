import pymunk

CELL_RADIUS = 3
CELL_COLOR = (0, 0, 0)

class Cell:
    def __init__(self, x, y, space): 
        self.body = pymunk.Body()
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, CELL_RADIUS)
        self.shape.elasticity = 0
        self.shape.density = 1
        self.shape.filer = pymunk.ShapeFilter(group=1)
        self.muscles = []
        space.add(self.body, self.shape)

    def draw(self, display):
        display.draw_circle(self.body.position, CELL_RADIUS, CELL_COLOR)
    
    def pos(self):
        x, y = self.body.position
        return (x, y)

    def apply_force(self, force):
        self.body.apply_force_at_local_point(force, (0, 0))

class CellFixed(Cell):
    def __init__(self, x, y, space):
        super().__init__(x, y, space)
        self.body.body_type = pymunk.Body.STATIC

