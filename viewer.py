import pygame
import simulation

SCREEN_SIZE = 600
FPS = 60

class Viewer:

    def __init__(self, simulation):
        pygame.init()
        self.py_display = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
        self.clock = pygame.time.Clock()
        self.FPS = FPS

        self.simulation = simulation
        self.display = Display(SCREEN_SIZE, (0, 0), self.py_display)
        self.simulation.addDisplay(self.display)

        self.running = True
        self.mouse_size = 20
        self.mouse_state = "UP"
        self.speed_up = False

    def run(self):
        while self.running:
            if not self.speed_up:
                self.clock.tick(self.FPS)

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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.speed_up = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_s:
                    self.speed_up = False

            self.simulation.handle_input(event)

    
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

    def draw(self):
        self.py_display.fill((255, 255, 255))
        self.display.draw_log("FPS: " + str(int(self.clock.get_fps())), (255, 0, 0))
        self.simulation.draw()
        self.display.draw_circle(self.mouse_pos(), self.mouse_size, (0, 0, 0), thickness=1)
        pygame.display.update()
        self.display.clear_log()

class Display:
        def __init__(self, screen_size, pos, display):
            self.screen_size = screen_size
            self.display = display
            self.pos = pos
            self.font_size = 18
            self.font = pygame.font.SysFont("Arial" , self.font_size , bold = True)
            self.log_y = 0

        def draw_circle(self, pos, radius, color, thickness=2):
            pygame.draw.circle(self.display, color, self.convert_coordinates(pos), radius, thickness)
        
        def draw_line(self, pos1, pos2, color, width):
            pygame.draw.line(self.display, color, self.convert_coordinates(pos1), self.convert_coordinates(pos2), width)
        
        def draw_text(self, text, pos, color):
            text = self.font.render(text, True, color)
            self.display.blit(text, pos) 
        
        def draw_log(self, text, color):
            self.draw_text(text, (self.font_size, self.log_y), color)
            self.log_y += self.font_size + 2
        
        def clear_log(self):
            self.log_y = 0


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
