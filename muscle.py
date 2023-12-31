import pymunk

MUSCLE_WIDTH = 2
CELL_HEIGHT = 20
CELL_WIDTH = 60

ENDODERM_STIFFNESS = 500
ENDODERM_MAX_FORCE = 1500
ENDODERM_DAMPING = 1000
ENDODERM_LENGTH = CELL_WIDTH
ENDODERM_COLOR = (255, 0, 0)

ECTODERM_STIFFNESS = 1000
ECTODERM_MAX_FORCE = 1500
ECTODERM_DAMPING = 1000
ECTODERM_LENGTH = CELL_HEIGHT
ECTODERM_COLOR = (0, 255, 0)

MAX_STIFFNESS = max(ENDODERM_STIFFNESS, ECTODERM_STIFFNESS)

EXCITATION_DECAY_RATE = 2

class Muscle:
    def __init__(self, cell1, cell2, space, stiffness, damping, length, max_force, color):
        self.body1 = cell1.body
        self.body2 = cell2.body
        cell1.muscles.append(self)
        cell2.muscles.append(self)

        self.color = color
        self.length = length
        self.stiffness = stiffness
        self.max_force = max_force

        self.excitation_duration = 0
        self.excitation = 0
        self.activation = 0

        joint1 = pymunk.DampedSpring(self.body1, self.body2,
                                            anchor_a=(0, 0), anchor_b=(0, 0),
                                            rest_length=length, stiffness=stiffness, damping=damping)
        space.add(joint1)


    def draw(self, display):
        width = int(MUSCLE_WIDTH * (self.stiffness / MAX_STIFFNESS))
        display.draw_line(self.body1.position, self.body2.position, self.color, width)

    
    def step(self, steps_size):
        activation =self.step_excitation(steps_size)
        force = -activation * self.max_force  * 20000

        self.body1.apply_force_at_local_point(self.muscle_vec() * force * steps_size, (0, 0))
        self.body2.apply_force_at_local_point(-self.muscle_vec() * force * steps_size, (0, 0))

    def excite(self, excitation, duration):
        self.excitation_duration = duration
        self.excitation += (excitation / duration)

    def step_excitation(self, steps_size):
        self.excitation_duration -= steps_size
        if self.excitation_duration < 0:
            self.excitation_duration = 0
            self.excitation = 0

        self.activation += self.excitation * steps_size

        self.activation -= self.activation * EXCITATION_DECAY_RATE * steps_size
        if abs(self.activation) < 0.0001:
            self.activation = 0
        return self.activation


    def push_muscle(self, force):
        self.body1.apply_force_at_local_point(force, (0, 0))
        self.body2.apply_force_at_local_point(force, (0, 0))

    def muscle_length(self):
        p1 = self.body1.position
        p2 = self.body2.position
        return (p1 - p2).length
    
    def muscle_vec(self):
        p1 = self.body1.position
        p2 = self.body2.position
        return (p1 - p2).normalized()
    
    def muscle_contained(self, pos, radius):
        pos = pymunk.Vec2d(pos[0], pos[1])

        if self.body1.position.get_distance(pos) < radius and self.body2.position.get_distance(pos) < radius:
            return True
        else:
            return False

class EndodermMuscle(Muscle):
    def __init__(self, cell1, cell2, space):
        super().__init__(cell1, cell2, space, ENDODERM_STIFFNESS, ENDODERM_DAMPING, ENDODERM_LENGTH, ENDODERM_MAX_FORCE, ENDODERM_COLOR)
        
class EctodermMuscle(Muscle):
    def __init__(self, cell1, cell2, side, space):
        super().__init__(cell1, cell2, space, ECTODERM_STIFFNESS, ECTODERM_DAMPING, ECTODERM_LENGTH, ECTODERM_MAX_FORCE, ECTODERM_COLOR)
        self.side = side