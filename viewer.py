import pygame
import simulation

SCREEN_SIZE = 600
FPS = 60

class Viewer:

    def __init__(self, simulation):
        pygame.init()
        self.display = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        self.simulation = simulation
        self.simulation.addDisplay(Display(SCREEN_SIZE, (0, 0), self.display))
        self.running = True
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial" , 18 , bold = True)
        self.mouse_size = 10
        self.mouse_state = "UP"

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.handle_mouse()
            self.simulation.step(FPS)
            self.draw()


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEWHEEL:
                self.mouse_size += event.y / -2
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse_state = "LEFT"
                elif event.button == 3:
                    self.mouse_state = "RIGHT"
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_state = "UP"
    
    def handle_mouse(self):
        if self.mouse_size < 0:
            self.mouse_size = 0

        if self.mouse_state == "LEFT": 
            self.simulation.mouse_muscles(self.mouse_pos(), self.mouse_size, 1)
        elif self.mouse_state == "RIGHT":
            self.simulation.mouse_muscles(self.mouse_pos(), self.mouse_size, -1)
    
    def mouse_pos(self):
        x, y = pygame.mouse.get_pos()
        return x - SCREEN_SIZE / 2, SCREEN_SIZE - y

    def draw_mouse(self):
        pygame.draw.circle(self.display, (90, 90, 90), pygame.mouse.get_pos(), self.mouse_size, 1)

    def draw(self):
        self.display.fill((255, 255, 255))
        self.simulation.draw()
        self.draw_mouse()
        self.fps_counter()
        pygame.display.update()
    
    def fps_counter(self):
        fps = self.font.render(str(int(self.clock.get_fps())), True, pygame.Color("coral"))
        self.display.blit(fps, (10, 10))

class Display:
        def __init__(self, screen_size, pos, display):
            self.screen_size = screen_size
            self.display = display
            self.pos = pos

        def draw_circle(self, pos, radius, color):
            pygame.draw.circle(self.display, color, self.convert_coordinates(pos), radius, 2)
        
        def draw_line(self, pos1, pos2, color, width):
            pygame.draw.line(self.display, color, self.convert_coordinates(pos1), self.convert_coordinates(pos2), width)


        def convert_coordinates(self, pos):
            x, y = pos
            return int(x) + self.screen_size / 2, self.screen_size - int(y)
    
if __name__ == "__main__":
    simulation = simulation.Simulation()
    simulation.createHydra()
    print("Simulation created")
    viewer = Viewer(simulation)
    print("Running viewer")
    viewer.run()
    pygame.quit()
