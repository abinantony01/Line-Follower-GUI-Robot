import pygame
import sys
from robot import Robot
from graphics import Graphics

pygame.init()

WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 720
FPS = 60

class Simulation:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("PID Line Follower Robot Simulation")
        self.clock = pygame.time.Clock()
        self.graphics = Graphics(self.screen)
        
        start_pos = (WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2)
        self.robot = Robot(start_pos[0], start_pos[1])
        self.graphics.load_custom_map("map.png")

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            sensor_readings = self.robot.read_sensors(self.graphics.map_surface)
            self.robot.update(sensor_readings)
            self.screen.fill((255, 255, 255))
            self.graphics.draw_map()
            self.graphics.draw_robot(self.robot)
            
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    simulation = Simulation()
    simulation.run()