import numpy as np
import pygame

class Config:
    pygame.init()
    pygame.font.init()  
    SCREEN = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
    FONT = pygame.font.SysFont('Comic Sans MS', 30)

    GREEN = (127,255,0)
    YELLOW = (255,255,51)
    WHITE = (255, 255, 255)
    SCREEN_X = SCREEN.get_width()
    SCREEN_Y = SCREEN.get_height()
    SPACESHIP_STARTING_Y = 750
    STARTING_POS_PLAYER_1 = (300, SPACESHIP_STARTING_Y)
    STARTING_POS_PLAYER_2 = (SCREEN_X-450, SPACESHIP_STARTING_Y)
    IMG_SPACESHIP_1 = "/home/adrian/Dokumenter/inf-1400/mayham/spaceships/a-03.png"
    IMG_SPACESHIP_2 = "/home/adrian/Dokumenter/inf-1400/mayham/spaceships/b-03.png"
    IMG_PLATFORM = "/home/adrian/Dokumenter/inf-1400/mayham/spaceships/platform.png"
    ORIGO = (0, 0)
    
    GRAVITY = 10
    SPACESHIP_SPEED = 70
    FUEL_REDUCTION = 70
    SPACESHIP_ROTATION_SPEED = 0.15
    MAX_FUEL = 200
    START_ANGLE = np.pi/2

    BULLET_RADIUS = 10
    BULLET_SPEED = 1000
    BULLET_COLOR = (150, 150, 150)

    OBSTACLE_WIDTH = 40
    OBSTACLE_HEIGHT = 330

    
    PLATFORM_1_POS = (STARTING_POS_PLAYER_1[0]-20, SPACESHIP_STARTING_Y+80)
    PLATFORM_2_POS = (STARTING_POS_PLAYER_2[0]-20, SPACESHIP_STARTING_Y+80)

    #Define the keys used for controlling the spaceships
    CONTROL_ARROWS = {
            "THRUST": pygame.K_UP,
            "LEFT": pygame.K_LEFT,
            "RIGHT": pygame.K_RIGHT,
            "BLASTER": pygame.K_SPACE
            }

    CONTROL_WAD = {
            "THRUST": pygame.K_w,
            "LEFT": pygame.K_a,
            "RIGHT": pygame.K_d,
            "BLASTER": pygame.K_LESS
            }

