import pymunk
import pygame
import hydra
from cell import Cell, CellFixed
from muscle import Muscle, EndodermMuscle, EctodermMuscle

PLATFORM_SIZE = 300
class Simulation:

    def __init__(self):
        self.space = pymunk.Space()
        self.display = None
        self.TIMESCALE = 1
        self.time = 0
        self.space.damping = 0.8

        self.cells = []
        self.muscles = []
        self.hydra = None

        floor = pymunk.Segment(self.space.static_body, (-PLATFORM_SIZE, 0), (PLATFORM_SIZE, 0), 2)
        self.space.add(floor)

    def addDisplay(self, display):
        self.display = display

    def displaySize(self):
        if self.display is not None:
            return self.display.screen_size

    def step(self, fps):
        self.space.step(self.TIMESCALE /fps)
        for muscle in self.muscles:
            muscle.step(self.TIMESCALE /fps)
        if self.hydra is not None:
            self.hydra.step(self.TIMESCALE / fps)
        
        self.time += self.TIMESCALE / fps


    def draw(self):
        if self.display is not None:
            self.display.draw_log(f"Time: {self.time:.2f}", (255, 0, 0))
            self.hydra.draw(self.display)
        

    def addCell(self, x, y):
        cell = Cell(x, y, self.space)
        self.cells.append(cell)
        return cell

    def addCellFixed(self, x, y):
        cell = CellFixed(x, y, self.space)
        self.cells.append(cell)
        return cell
    
    def addEndodermMuscle(self, cell1, cell2):
        muscle = EndodermMuscle(cell1, cell2, self.space)
        self.muscles.append(muscle)
        return muscle
    
    def addEctodermMuscle(self, cell1, cell2, side):
        muscle = EctodermMuscle(cell1, cell2, side, self.space)
        self.muscles.append(muscle)
        return muscle
    
    def createHydra(self):
        self.hydra = hydra.Hydra(self.space)
        self.cells.extend(self.hydra.cells)
        self.muscles.extend(self.hydra.endoderm_muscles)
        self.muscles.extend(self.hydra.ectoderm_muscles)
        
    
    def mouse_muscles(self, pos, radius, amount):
        for muscle in self.muscles:

            if muscle.muscle_contained(pos, radius):
                muscle.excite(amount)
    
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                self.hydra.contract()
            if event.key == pygame.K_e:
                self.hydra.elongate()

                
