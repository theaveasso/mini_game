import math
import pygame
from pygame.math import Vector2

from utils import blit_rotate_center, scale

# game assets
COM_CAR = scale(pygame.image.load('assets/car_02.png'), .5)
PLAYER_CAR = scale(pygame.image.load('assets/car_01.png'), .5)

        
class AbstractCar:
    def __init__(self):
        self.img = self.IMG
        self.angle = 0
        self.length = 4
        self.sterring = 0.
        self.max_steering = 30
        self.acceleration = 0.
        self.max_acceleration = 2.
        self.max_velocity = 20
        self.velocity = Vector2(0., 0.)
        self.free_deceleration = 2
        self.brake_deceleration = 10
        self.position = Vector2(self.START_POS[0], self.START_POS[1])

    def update(self, dt):
        self.velocity -= (0, self.acceleration * dt)
        # velocity limit
        self.velocity.y = max(-self.max_velocity, min(self.velocity.y, self.max_velocity))
        
        if self.sterring:
            turning_rad = self.length / math.sin(math.radians(self.sterring))
            angular_velocity = self.velocity.x / turning_rad
        else:
            angular_velocity = 0
        
        self.position -= self.velocity.rotate(-self.angle) * dt
        self.angle += math.degrees(angular_velocity) * dt

    def draw(self, screen):
        rotated = pygame.transform.rotate(self.img, self.angle)
        rect = rotated.get_rect()
        screen.blit(rotated, self.position * 32 - (rect.width / 2, rect.height / 2))
        
class PlayerCar(AbstractCar):
    IMG = PLAYER_CAR
    START_POS = (150, 200)
        

        
        
