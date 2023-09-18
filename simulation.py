import pymunk
import hydra

TIMESCALE = 1
CELL_RADIUS = 4
CELL_COLOR = (0, 0, 0)

HYDRA_HEIGHT = 20
CELL_HEIGHT = 20
CELL_WIDTH = 60

MUSCLE_WIDTH = 2

ENDODERM_STIFFNESS = 1000
ENDODERM_DAMPING = 1000
ENDODERM_LENGTH = CELL_WIDTH
ENDODERM_COLOR = (0, 255, 0)

ECTODERM_STIFFNESS = 1000
ECTODERM_DAMPING = 1000
ECTODERM_LENGTH = CELL_HEIGHT
ECTODERM_COLOR = (255, 0, 0)

MAX_STIFFNESS = max(ENDODERM_STIFFNESS, ECTODERM_STIFFNESS)


class Simulation:

    def __init__(self):
        self.space = pymunk.Space()
        #self.space.damping = 0.1
        self.display = None

        self.cells = []
        self.muscles = []
        self.hydra = None

    def addDisplay(self, display):
        self.display = display

    def displaySize(self):
        if self.display is not None:
            return self.display.screen_size

    def step(self, steps_size):
        self.space.step(TIMESCALE /steps_size)

    def draw(self):
        if self.display is not None:
            for cell in self.cells:
                cell.draw(self.display)
            
            for muscle in self.muscles:
                muscle.draw(self.display)

    def addCell(self, x, y):
        cell = Cell(x, y, self.space)
        self.cells.append(cell)
        return cell

    def addCellFixed(self, x, y):
        cell = CellFixed(x, y, self.space)
        self.cells.append(cell)
        return cell
    
    def addEndodermMuscle(self, cell1, cell2):
        self.muscles.append(EndodermMuscle(cell1, cell2, self.space))
    
    def addEctodermMuscle(self, cell1, cell2):
        self.muscles.append(EctodermMuscle(cell1, cell2, self.space))
    
    def createHydra(self):
        self.hydra = hydra.Hydra(HYDRA_HEIGHT)

        left =   - (CELL_WIDTH / 2)
        right = (CELL_WIDTH / 2)

        fc1 = self.addCellFixed(left, 2)
        fc2 = self.addCellFixed(right, 2)
        self.hydra.cells.extend([fc1, fc2])
        self.hydra.layers.append((fc1, fc2))

        for i in range(1, self.hydra.height):
            c1 = self.addCell(left, i * CELL_HEIGHT + 2)
            c2 = self.addCell(right, i * CELL_HEIGHT + 2)
            self.hydra.muscles.append(self.addEndodermMuscle(c1, c2))

            b1, b2 = self.hydra.layers[i - 1]
            self.hydra.muscles.append(self.addEctodermMuscle(b1, c1))
            self.hydra.muscles.append(self.addEctodermMuscle(b2, c2))

            self.hydra.layers.append((c1, c2))
            self.hydra.muscles.extend([c1,c2])
        
        self.hydra.volume = self.hydra.calc_volume()
    
    def mouse_muscles(self, pos, radius, amount):
        for cell in self.cells:
            x = pos[0] - cell.pos()[0]
            y = pos[1] - cell.pos()[1]
            if x ** 2 + y ** 2 < radius ** 2:
                cell.body.apply_force_at_local_point((0, 2000 * -amount))

class Cell:
    def __init__(self, x, y, space): 
        self.body = pymunk.Body()
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, CELL_RADIUS)
        self.shape.elasticity = 0
        self.shape.density = 1
        space.add(self.body, self.shape)

    def draw(self, display):
        display.draw_circle(self.body.position, CELL_RADIUS, CELL_COLOR)
    
    def pos(self):
        x, y = self.body.position
        return (x, y)

class CellFixed(Cell):
    def __init__(self, x, y, space):
        super().__init__(x, y, space)
        self.body.body_type = pymunk.Body.STATIC

class Muscle:
    def __init__(self, cell1, cell2, space, stiffness, damping, length, color):
        self.body1 = cell1.body
        self.body2 = cell2.body
        self.color = color
        self.length = length
        self.stiffness = stiffness

        joint1 = pymunk.DampedSpring(self.body1, self.body2,
                                    anchor_a=(0, 0), anchor_b=(0, 0),
                                    rest_length=length, stiffness=stiffness, damping=damping)
        space.add(joint1)

    def draw(self, display):
        width = int(MUSCLE_WIDTH * (self.stiffness / MAX_STIFFNESS))
        display.draw_line(self.body1.position, self.body2.position, self.color, width)

class EndodermMuscle(Muscle):
    def __init__(self, cell1, cell2, space):
        super().__init__(cell1, cell2, space, ENDODERM_STIFFNESS, ENDODERM_DAMPING, ENDODERM_LENGTH, ENDODERM_COLOR)
        
class EctodermMuscle(Muscle):
    def __init__(self, cell1, cell2, space):
        super().__init__(cell1, cell2, space, ECTODERM_STIFFNESS, ECTODERM_DAMPING, ECTODERM_LENGTH, ECTODERM_COLOR)

