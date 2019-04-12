import pygame
import numpy as np
from config import Config

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, screen, img, controls, start_pos, color):
        super().__init__()
        self.img = pygame.image.load(img).convert_alpha()
        self.screen = screen
        self.height = self.img.get_height()
        self.width = self.img.get_width()
        self.start_pos = start_pos
        self.x, self.y = start_pos
        self.speed_x, self.speed_y = Config.ORIGO
        self.accel = 0
        self.fueling = False
        self.controls = controls
        self.color = color
        self.bullets = pygame.sprite.Group()
        self.score = 0
        self.angle = Config.START_ANGLE
        self.gravity = Config.GRAVITY
        self.fuel = Config.MAX_FUEL
        self.rect = self.draw()

    def draw(self):
        img, rect = self.rot_center()

        return self.screen.blit(img, rect) 

    def rot_center(self):
        cent = (self.x + (self.width/2), self.y + (self.height/2))
        rot_image = pygame.transform.rotate(
                self.img, np.rad2deg(self.angle+np.pi/2))
        rot_rect = rot_image.get_rect(center=cent)

        return rot_image, rot_rect

    def wall_collision_handler(self):
        """Resets spaceship if it collides with one of the
        screen walls"""
        if self.x + self.height > self.screen.get_width(): 
            self.reset()
        elif self.x < 0: 
            self.reset()
        elif self.y + self.height > self.screen.get_height(): 
            self.reset()
        elif self.y < 0: 
            self.reset()

    def movement(self, time_passed):
        """Handles spaceship movement, the y-direction has an additional
        component gravity which makes the spaceship accelerate
        downwards"""
        self.speed_x += np.cos(self.angle) * self.accel * time_passed
        self.speed_y += ((-np.sin(self.angle) \
                * self.accel) \
                + self.gravity) \
                * time_passed
        self.x += self.speed_x
        self.y += self.speed_y

    def spaceship_cockpit_coordinates(self):
        """Calculates and returns the position of the 'cockpit' when
        the spaceship rotates"""
        rot_mat = np.array([[np.cos(self.angle), -1*np.sin(self.angle)],
                            [np.sin(self.angle), np.cos(self.angle)]])
        pos = np.array([(self.width/2), 0])
        rot = pos@rot_mat
        cent = [self.x + self.width/2, self.y + self.height/2]
        
        return (np.array(cent) + rot).tolist()

    def fuel_empty(self):
        """calles reset if the spaceship has no fuel left"""
        if self.fuel <= 0:
            self.reset()

    def update(self, time_passed):
        """handles all updates"""
        self.movement(time_passed)
        self.wall_collision_handler()
        self.fuel_empty()
        self.rect = self.draw()

    def reset(self, hit_by_bullet = False):
        """reset the state of the spaceship"""
        self.x, self.y = self.start_pos
        self.speed_x, self.speed_y = Config.ORIGO
        self.accel = 0
        self.angle = Config.START_ANGLE
        self.fuel = Config.MAX_FUEL
        if not hit_by_bullet:
            self.score -= 1
