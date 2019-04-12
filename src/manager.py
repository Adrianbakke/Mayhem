import numpy as np
import pygame
from spaceship import Spaceship
from bullet import Bullet
from platform import Platform
from obstacle import Obstacle
from config import Config

screen = Config.SCREEN 
myfont = Config.FONT
clock = pygame.time.Clock()

class Manager:
    def __init__(self):
        #initialize spaceships
        self.player_1_spaceship = Spaceship(
                screen,
                Config.IMG_SPACESHIP_1,
                Config.CONTROL_WAD,
                Config.STARTING_POS_PLAYER_1,
                Config.YELLOW)
        self.player_2_spaceship = Spaceship(
                screen,
                Config.IMG_SPACESHIP_2,
                Config.CONTROL_ARROWS,
                Config.STARTING_POS_PLAYER_2,
                Config.GREEN)

        self.spaceships = [self.player_1_spaceship,
                self.player_2_spaceship]

        self.spaceship_group = pygame.sprite.Group()

        for s in self.spaceships:
            self.spaceship_group.add(s)

        #initialize platforms
        self.platform_1 = Platform(screen, Config.PLATFORM_1_POS)
        self.platform_2 = Platform(screen, Config.PLATFORM_2_POS)

        self.platforms = [self.platform_1, self.platform_2]

        self.platform_group = pygame.sprite.Group()

        for p in self.platforms:
            self.platform_group.add(p)

        #initialize obstacle
        self.obstacle = Obstacle(screen)

        #quit instructions
        self.textsurface = myfont.render(
                "press 'q' to quit", False, Config.WHITE)

    def gameloop(self):
        """Runs the game"""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            time_passed = clock.tick(30) / 1000.0
            screen.fill((0,0,0))
            keys = pygame.key.get_pressed()

            if keys[pygame.K_q]:
                running = False

            self.update(keys, time_passed)
            self.display()

            pygame.display.update()

    def rotate_spaceship(self, spaceship, keys):
        """Rotates spaceship left or right depending on the key
        the user presses"""
        if keys[spaceship.controls["LEFT"]]:
            spaceship.angle += Config.SPACESHIP_ROTATION_SPEED

        elif keys[spaceship.controls["RIGHT"]]:
            spaceship.angle -= Config.SPACESHIP_ROTATION_SPEED 

    def thrust(self, spaceship, keys, time_passed):
        """Acclerate spaceship when thrust key is pressed"""
        if keys[spaceship.controls["THRUST"]]:
            spaceship.accel = Config.SPACESHIP_SPEED
            spaceship.fuel -= Config.FUEL_REDUCTION * time_passed
            spaceship.fueling = False
        else:
            spaceship.accel = 0

    def gravity(self, spaceship):
        """If the spaceship is fueling the 'gravity' is disabled
        to keep the spaceship from falling through the platform.
        If the spaceship is not fueling and gravity is set to zero then
        gravity is enabled"""
        if spaceship.fueling:
            spaceship.gravity = 0
        elif spaceship.gravity == 0:
            spaceship.gravity = Config.GRAVITY 

    def blaster(self, spaceship, keys):
        """Creats bullets and adds them to the spaceship.bullets group
        when the user presses the blaster key"""
        if keys[spaceship.controls["BLASTER"]]:
            pos = spaceship.spaceship_cockpit_coordinates()
            spaceship.bullets.add(
                    Bullet(screen, pos, spaceship.angle))

    def hit_by_bullet(self):
        """If a player hits the other players spaceship with
        a bullet the score increases with 1 and the spaceship
        which was hit resets"""
        p1_hit = pygame.sprite.spritecollide(
                self.player_1_spaceship,
                self.player_2_spaceship.bullets, True)
        p2_hit = pygame.sprite.spritecollide(
                self.player_2_spaceship,
                self.player_1_spaceship.bullets, True)

        if p1_hit and not self.player_1_spaceship.fueling:
            self.player_1_spaceship.reset(hit_by_bullet = True)
            self.player_2_spaceship.score += 1
        if p2_hit and not self.player_2_spaceship.fueling:
            self.player_2_spaceship.reset(hit_by_bullet = True)
            self.player_1_spaceship.score += 1

    def hit_obstacle(self):
        """If spaceship hits obstacle then the spaceship resets and
        score i lowered by 1. If a bullet hits the obstacle then the
        bullet is absorbed"""
        pygame.sprite.spritecollide(
                self.obstacle,
                self.player_1_spaceship.bullets, True)
        pygame.sprite.spritecollide(
                self.obstacle,
                self.player_2_spaceship.bullets, True)

        p1_collide = pygame.sprite.collide_rect(
                self.player_1_spaceship,
                self.obstacle)
        p2_collide = pygame.sprite.collide_rect(
                self.player_2_spaceship,
                self.obstacle)

        if p1_collide:
            self.player_1_spaceship.reset()
        if p2_collide:
            self.player_2_spaceship.reset()

    def spaceship_on_platform(self, time_passed):
        """If the spaceship is one the platform then the fuel will
        be filled if the fuel is not already on max. The spaceship will
        also be rotated so its 'cockpit' faces up"""
        for s in self.spaceships:
            s_on_platform = pygame.sprite.spritecollide(
                    s,
                    self.platform_group,
                    False)

            if s_on_platform:
                s.speed_x = 0
                s.speed_y = 0
                s.fueling = True
                self.spaceship_face_up(s)
                s.y = Config.SPACESHIP_STARTING_Y - 1

            if s.fueling and s.fuel < Config.MAX_FUEL:
                s.fuel += 100 * time_passed
                if s.fuel > Config.MAX_FUEL:
                    s.fuel = Config.MAX_FUEL 

            if s.y < Config.SPACESHIP_STARTING_Y-1:
                s.fueling = False

    def spaceship_face_up(self, spaceship):
        """Takes care of the rotation needed to make the
        'cockpit' face upward"""
        angle = spaceship.angle - np.pi/2
        twoPI = 2*np.pi

        if angle > twoPI:
            angle -= twoPI * abs(int(angle/twoPI))
        elif angle < -twoPI:
            angle += twoPI * abs(int(angle/twoPI))

        if angle > np.pi:
            angle -= twoPI
        elif angle < -np.pi:
            angle += twoPI

        if angle < 0:
            spaceship.angle += 2*Config.SPACESHIP_ROTATION_SPEED
            angle += 2*Config.SPACESHIP_ROTATION_SPEED 
            if angle > 0:
                spaceship.angle = np.pi/2
        elif angle > 0:
            spaceship.angle -= 2*Config.SPACESHIP_ROTATION_SPEED 
            angle -= 2*Config.SPACESHIP_ROTATION_SPEED 
            if angle < 0:
                spaceship.angle = np.pi/2

    def display_fuel(self):
        """Shows how much fuel is left"""
        x_pos = [50, Config.SCREEN_X-250]
        comb = zip(self.spaceships, x_pos)
        for s,x in comb:
            pygame.draw.line(
                    screen, 
                    s.color,
                    (x, 50),
                    (x + s.fuel, 50),
                    10)
            
    def display_quit_instructions(self):
        screen.blit(self.textsurface, (Config.SCREEN_X/2, 30))

    def display_score(self):
        """Shows the score the players has obtained"""
        x_pos = [50, Config.SCREEN_X-250]
        comb = zip(self.spaceships, x_pos)
        for s,x in comb:
            score = myfont.render(
                    "Score: {}".format(s.score),
                    False,
                    (255, 255, 255))

            screen.blit(score, (x, 70))
                
    def update(self, keys, time_passed):
        """Takes care of all updates"""
        for s in self.spaceships:
            self.rotate_spaceship(s, keys)
            self.thrust(s, keys, time_passed)
            self.gravity(s)
            self.blaster(s, keys)
        
        self.hit_by_bullet()
        self.spaceship_on_platform(time_passed)
        self.hit_obstacle()

        self.player_1_spaceship.bullets.update(time_passed)
        self.player_2_spaceship.bullets.update(time_passed)
        self.spaceship_group.update(time_passed)
        self.platform_group.update()
        self.obstacle.update()

    def display(self):
        """Takes care of all displays"""
        self.display_fuel()
        self.display_quit_instructions()
        self.display_score()
