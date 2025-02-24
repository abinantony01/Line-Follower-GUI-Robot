import pygame
import math
import numpy as np

class Graphics:
    def __init__(self, screen):
        self.screen = screen
        self.map_surface = pygame.Surface(screen.get_size())
        self.map_surface.fill((255, 255, 255))
        
        try:
            self.robot_image = pygame.image.load("robot.png").convert_alpha()
            self.robot_image = pygame.transform.scale(self.robot_image, (80, 80))
        except pygame.error:
            print("Could not load robot.png - using default rectangle")
            self.robot_image = None

    def create_spiral_map(self):
        center_x = self.screen.get_width() // 2
        center_y = self.screen.get_height() // 2
        theta = 0
        radius = 10
        points = []
        
        while radius < min(center_x, center_y) - 50:
            x = center_x + radius * math.cos(theta)
            y = center_y + radius * math.sin(theta)
            points.append((int(x), int(y)))
            theta += 0.1
            radius += 0.5

        if len(points) > 1:
            pygame.draw.lines(self.map_surface, (0, 0, 0), False, points, 2)

    def load_custom_map(self, filename):
        try:
            loaded_map = pygame.image.load(filename)
            scaled_map = pygame.transform.scale(
                loaded_map, 
                self.screen.get_size()
            )
            self.map_surface.blit(scaled_map, (0, 0))
        except pygame.error as e:
            print(f"Error loading map: {e}")
            self.create_spiral_map()
    def draw_map(self):
        self.screen.blit(self.map_surface, (0, 0))

    def draw_robot(self, robot):
        if self.robot_image:
            angle = math.degrees(-robot.heading)
            rotated_image = pygame.transform.rotate(self.robot_image, angle)
            rect = rotated_image.get_rect()
            rect.center = (int(robot.x), int(robot.y))
            self.screen.blit(rotated_image, rect)
        else:
            points = self._get_robot_corners(robot)
            pygame.draw.polygon(self.screen, (100, 100, 255), points)
        
        sensor_positions = robot._get_sensor_positions()
        for pos in sensor_positions:
            pygame.draw.circle(self.screen, (255, 0, 0), 
                             (int(pos[0]), int(pos[1])), 3)

    def _get_robot_corners(self, robot):
        cos_h = math.cos(robot.heading)
        sin_h = math.sin(robot.heading)
        
        corners = [
            (-robot.width/2, -robot.length/2),
            (robot.width/2, -robot.length/2),
            (robot.width/2, robot.length/2),
            (-robot.width/2, robot.length/2)
        ]
        
        transformed = []
        for x, y in corners:
            rotated_x = x * cos_h - y * sin_h
            rotated_y = x * sin_h + y * cos_h
            transformed.append((
                int(robot.x + rotated_x),
                int(robot.y + rotated_y)
            ))
            
        return transformed