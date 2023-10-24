from math import sqrt, pow, log
from cell import Cell, CellFixed
from muscle import EndodermMuscle, EctodermMuscle
import pymunk
import numpy as np

import torch
import torch.nn as nn
from learning.motor_control import MotorControl

WATER_BULK_MODULUS = 2.15 * pow(10, 5)

HYDRA_HEIGHT = 15
CELL_HEIGHT = 20
CELL_WIDTH = 60

class Hydra:

    def __init__(self, space):
        self.height = HYDRA_HEIGHT

        self.cells = []
        self.layers = []
        self.endoderm_muscles = []
        self.ectoderm_muscles = []
        self.roof = None

        self.brain = None

        self.area = -1
        self.original_head_pos = None
        self.status = "STABLE"

        left =   - (CELL_WIDTH / 2)
        right = (CELL_WIDTH / 2)

        fc1 = CellFixed(left, 2, space)
        fc2 = CellFixed(right, 2, space)
        self.cells.extend([fc1, fc2])
        self.layers.append((fc1, fc2))

        for i in range(1, self.height):
            c1 = Cell(left, i * CELL_HEIGHT + 2, space)
            c2 = Cell(right, i * CELL_HEIGHT + 2, space)
            self.endoderm_muscles.append(EndodermMuscle(c1, c2, space))

            b1, b2 = self.layers[i - 1]
            self.ectoderm_muscles.append(EctodermMuscle(b1, c1, "LEFT", space))
            self.ectoderm_muscles.append(EctodermMuscle(b2, c2, "RIGHT", space))

            self.layers.append((c1, c2))
            self.cells.extend((c1, c2))
        
        self.roof = self.endoderm_muscles[-1]
        pin = pymunk.PinJoint(self.roof.body1, self.roof.body2, (0, 0), (0, 0))
        space.add(pin)

        self.original_head_pos = (self.roof.body1.position + self.roof.body2.position) / 2
        print(self.original_head_pos)
        self.area = self.calc_area()
    
    def get_status(self):
        spd = self.roof.body1.velocity.length
        head = (self.roof.body1.position + self.roof.body2.position) / 2
        dist = head.get_distance(self.original_head_pos)

        if spd < 5 and dist < 100:
            self.status = "STABLE"
        elif spd <2:
            self.status = "STUCK"
        elif spd > 500 or dist > 500:
            self.status = "EXPLODING"
        else:
            self.status = "MOVING"

    def calc_area(self):
        area = 0
        for i in range(1, len(self.layers)):
            l11, l12 = self.layers[i - 1]
            l21, l22 = self.layers[i]

            l11 = l11.body.position
            l12 = l12.body.position
            l21 = l21.body.position
            l22 = l22.body.position

            area += calc_area_quad(l11, l12, l21, l22)
        return area

    def calc_peri(self):
        peri = 0
        for muscle in self.ectoderm_muscles:
            peri += muscle.muscle_length()
        return peri

    def calc_length(self):
        diff1 = self.layers[0][0].body.position - self.roof.body1.position
        diff2 = self.layers[0][1].body.position - self.roof.body2.position

        return (diff1.length + diff2.length) / 2

    def step(self, step_size):
        self.get_status()
        pressure = self.calc_pressure(self.calc_area())

        if pressure > 100:
            self.push_walls(pressure, step_size)

    def calc_pressure(self, area):
        return - WATER_BULK_MODULUS * log(area / self.area)

    def calc_center(self, layer):
        p1 = self.layers[layer][0].body.position
        p2 = self.layers[layer][1].body.position
        return (p1 + p2) / 2

    def push_walls(self, pressure, step_size):
        for layer in self.layers:
            cell1 = layer[0]
            cell2 = layer[1]

            norm =(cell1.body.position - cell2.body.position).normalized()
            length1 = sum([x.muscle_length() for x in cell1.muscles])
            length2 = sum([x.muscle_length() for x in cell2.muscles])
            cell1.apply_force(norm * length1 * pressure * step_size)
            cell2.apply_force(-norm * length2 *pressure * step_size)

        force = -self.roof.muscle_length() * pressure * self.roof.muscle_vec().perpendicular()
        self.roof.push_muscle(force * step_size)


    def draw(self, display):
        for muscle in self.endoderm_muscles:
            muscle.draw(display)
        for muscle in self.ectoderm_muscles:
            muscle.draw(display)
        for cell in self.cells:
            cell.draw(display)

        #display.draw_log(f"Length: {self.calc_length():.2f}", (0, 0, 0))
        #display.draw_log(f"Pressure: {self.calc_pressure(self.calc_area()):.2f}", (0, 0, 0))
        #display.draw_log(f"Status: {self.status}", (0, 0, 0))
        
    def contract(self):
        for muscle in self.ectoderm_muscles:
            muscle.excite(0.5, 5)
    
    def elongate(self):
        for muscle in self.endoderm_muscles:
            muscle.excite(0.5, 10)

    def play_excitation(self, map):
        for i in range(HYDRA_HEIGHT - 1):
            self.ectoderm_muscles[i * 2].excite(map[i][0], 15)
            self.ectoderm_muscles[i * 2 + 1].excite(map[i][2], 15)
            self.endoderm_muscles[i].excite(map[i][1], 15)

    def get_excitation(self):
        map = np.zeros((HYDRA_HEIGHT - 1, 3))
        for i in range(HYDRA_HEIGHT - 1):
            map[i][0] = self.ectoderm_muscles[i * 2].activation
            map[i][2] = self.ectoderm_muscles[i * 2 + 1].activation
            map[i][1] = self.endoderm_muscles[i].activation
        return map
    
    def play_input(self, activation_map):
        if self.brain == None:
            print("")
            return
        self.brain.eval()
        flatten = activation_map.flatten(order="F")
        response = self.brain(torch.tensor(flatten, dtype=torch.float32))

        map = response.detach().numpy()
        map = map.reshape((HYDRA_HEIGHT - 1, 3), order='F')
        self.play_excitation(map)
        return map

    def load_brain(self, model_state_path):
        self.brain = MotorControl()
        self.brain.load_state_dict(torch.load(model_state_path))


def calc_area_quad(p11, p12, p21, p22):
    return calc_area_tri(p11, p12, p21) + calc_area_tri(p12, p21, p22)

def calc_area_tri(p1, p2, p3):
    s1 = p1 - p2
    s2 = p2 - p3
    s3 = p3 - p1
    s1 = s1.length
    s2 = s2.length
    s3 = s3.length
    return (s2 * sqrt(s1**2 - ((s1**2 + s2**2 - s3**2) / (2*s2))**2)) / 2

