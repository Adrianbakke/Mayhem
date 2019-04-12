import pygame
from config import Config

class Obstacle:
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.rect = self.draw()

    def draw(self):
        """draws obstacle"""
        return pygame.draw.rect(
                self.screen,
                (255, 0, 0),
                pygame.Rect(
                    self.width/2-Config.OBSTACLE_WIDTH/2,
                    300,
                    Config.OBSTACLE_WIDTH,
                    Config.OBSTACLE_HEIGHT))

    def update(self):
        """handles updates"""
        self.draw()
        
