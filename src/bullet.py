import pygame
import numpy as np
from config import Config

class Bullet(pygame.sprite.Sprite):
    def __init__(self, screen, pos, angle):
        super().__init__()
        self.screen = screen
        self.radius = Config.BULLET_RADIUS
        self.angle = angle
        self.x, self.y = pos
        self.speed_x, self.speed_y = Config.ORIGO 
        self.speed_const = Config.BULLET_SPEED
        self.color = Config.BULLET_COLOR
        self.rect = self.draw()

    def draw(self):
        """draws bullet"""
        return pygame.draw.circle(
                self.screen,
                self.color,
                (int(self.x), int(self.y)),
                self.radius)

    def movement(self, time_passed):
        """Bullets have constant speed"""
        self.speed_x = np.cos(self.angle) \
                * self.speed_const \
                * time_passed
        self.speed_y = -np.sin(self.angle) \
                * self.speed_const \
                * time_passed
        self.x += self.speed_x
        self.y += self.speed_y

    def wall_collision_handler(self):
        """Bullets which hit the screen walls are absorbed"""
        if self.x + self.radius > self.screen.get_width(): 
            self.kill()
        elif self.x - self.radius < 0: 
            self.kill()
        elif self.y + self.radius > self.screen.get_height(): 
            self.kill()
        elif self.y - self.radius < 0: 
            self.kill()

    def update(self, time_passed):
        """handles updates"""
        self.movement(time_passed)
        self.wall_collision_handler()
        self.rect = self.draw()
