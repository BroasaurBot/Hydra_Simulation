import pymunk
from openmuscle import Muscle as OpenMuscle

MUSCLE_WIDTH = 2
CELL_HEIGHT = 20
CELL_WIDTH = 60

ENDODERM_STIFFNESS = 1000
ENDODERM_MAX_FORCE = 32.0
ENDODERM_DAMPING = 1000
ENDODERM_LENGTH = CELL_WIDTH
ENDODERM_COLOR = (0, 255, 0)

ECTODERM_STIFFNESS = 1000
ECTODERM_MAX_FORCE = 32.0
ECTODERM_DAMPING = 1000
ECTODERM_LENGTH = CELL_HEIGHT
ECTODERM_COLOR = (255, 0, 0)

MAX_STIFFNESS = max(ENDODERM_STIFFNESS, ECTODERM_STIFFNESS)


class Muscle:
    def __init__(self, cell1, cell2, space, stiffness, damping, length, color):
        self.body1 = cell1.body
        self.body2 = cell2.body
        self.color = color
        self.length = length
        self.stiffness = stiffness
        self.excitation = 0.0001

        self.muscle = OpenMuscle(0)
        self.length0 = length

    def draw(self, display):
        width = int(MUSCLE_WIDTH * (self.stiffness / MAX_STIFFNESS))
        display.draw_line(self.body1.position, self.body2.position, self.color, width)
    
    def step(self, steps_size):
        curr_length = self.muscle_length()
        rel_length = curr_length / self.length

        change_length = curr_length - self.length0
        vel = change_length / steps_size

        force = self.muscle.calc_force(self.excitation, rel_length, vel, steps_size)
        print(force)

        #self.body1.apply_force_at_local_point(-force * self.muscle_vec(), (0, 0))
        #self.body2.apply_force_at_local_point(force * self.muscle_vec(), (0, 0))

        self.length0 = curr_length

    
    def muscle_length(self):
        p1 = self.body1.position
        p2 = self.body2.position
        return (p1 - p2).length
    
    def muscle_vec(self):
        p1 = self.body1.position
        p2 = self.body2.position
        return (p1 - p2).unit()

class EndodermMuscle(Muscle):
    def __init__(self, cell1, cell2, space):
        super().__init__(cell1, cell2, space, ENDODERM_STIFFNESS, ENDODERM_DAMPING, ENDODERM_LENGTH, ENDODERM_COLOR)
        
class EctodermMuscle(Muscle):
    def __init__(self, cell1, cell2, space):
        super().__init__(cell1, cell2, space, ECTODERM_STIFFNESS, ECTODERM_DAMPING, ECTODERM_LENGTH, ECTODERM_COLOR)