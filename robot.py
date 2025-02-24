import math
import pygame
import numpy as np

class Robot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.heading = 0
        self.width = 60
        self.length = 80
        
        #controller parameters
        self.base_speed = 2  # Reduced for better control
        self.Kp = 2.5  # Increased for stronger correction (P)
        self.Ki = 0.01  # Integral gain                    (I)
        self.Kd = 0.5  # Derivative gain                   (D)
        
        # PID controller state
        self.integral = 0
        self.last_error = 0
        self.off_line_counter = 0
        
        self.sensor_spread = 15  # Reduced spread for better line detection
        self.sensor_forward_offset = 40  # Increased forward offset for earlier detection

    def read_sensors(self, map_surface):
        sensors = self._get_sensor_positions()
        readings = []
        
        for sensor_x, sensor_y in sensors:
            try:
                readings.append(self._get_average_reading(map_surface, sensor_x, sensor_y))
            except IndexError:
                readings.append(0)
        
        return readings

    def _get_average_reading(self, map_surface, x, y):
        total = 0
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                try:
                    px = int(x + dx)
                    py = int(y + dy)
                    if 0 <= px < map_surface.get_width() and 0 <= py < map_surface.get_height():
                        color = map_surface.get_at((px, py))
                        total += 1 if color[0] < 128 else 0
                        count += 1
                except IndexError:
                    continue
        
        return 1 if count > 0 and (total / count) > 0.3 else 0

    def _get_sensor_positions(self):
        cos_h = math.cos(self.heading)
        sin_h = math.sin(self.heading)
    
        center_x = self.x + self.sensor_forward_offset * cos_h
        center_y = self.y + self.sensor_forward_offset * sin_h
        
        left_x = center_x - self.sensor_spread * sin_h
        left_y = center_y + self.sensor_spread * cos_h
        right_x = center_x + self.sensor_spread * sin_h
        right_y = center_y - self.sensor_spread * cos_h
        
        return [(left_x, left_y), (center_x, center_y), (right_x, right_y)]

    def update(self, sensor_readings):
        error = 0
        
        if sum(sensor_readings) == 0:
            self.off_line_counter += 1
            if self.off_line_counter > 10:  
                error = self.last_error * 1.5  
                self.integral *= 0.5  
        else:
            self.off_line_counter = 0
            # Weighted error calculation
            error = (-sensor_readings[0] + sensor_readings[2])
            if sensor_readings[1]: 
                error *= 0.5
            
            self.integral = max(-2, min(2, self.integral + error * 0.1))
            derivative = error - self.last_error
            
            error = (self.Kp * error + 
                    self.Ki * self.integral + 
                    self.Kd * derivative)
            
            self.last_error = error

        left_speed = self.base_speed + error
        right_speed = self.base_speed - error

        max_speed = 4
        left_speed = max(-max_speed, min(max_speed, left_speed))
        right_speed = max(-max_speed, min(max_speed, right_speed))

        average_speed = (left_speed + right_speed) / 2
        angular_velocity = (right_speed - left_speed) / self.width
        
        self.x += average_speed * math.cos(self.heading)
        self.y += average_speed * math.sin(self.heading)
        self.heading += angular_velocity
        
        self.heading = self.heading % (2 * math.pi)
