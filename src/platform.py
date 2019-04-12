import pygame
from config import Config

class Platform(pygame.sprite.Sprite):
    def __init__(self, screen, pos):
        super().__init__()
        self.screen = screen
        self.img = pygame.image.load(Config.IMG_PLATFORM).convert()
        self.pos = pos
        self.rect = self.draw()
        
    def draw(self):
        """draws platform"""
        return self.screen.blit(self.img, self.pos) 

    def update(self):
        """handle updates"""
        self.draw()

