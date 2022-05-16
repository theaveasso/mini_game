import random
from secrets import choice
import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 480, 800

class BG(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        bg_image = pygame.image.load('assets/graphics/environment/background.png')

        full_width = bg_image.get_width() * scale_factor
        full_height = bg_image.get_height() * scale_factor
        full_size_image = pygame.transform.scale(bg_image, (full_width, full_height))

        self.image = pygame.Surface((full_width * 2, full_height))
        self.image.blit(full_size_image, (0, 0))
        self.image.blit(full_size_image, (full_width, 0))
        self.rect = self.image.get_rect(topleft = (0, 0))
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self, dt):
        self.pos.x -= 300 * dt
        if self.rect.centerx < 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)

class FG(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        self.sprite_type = 'other'
        # load and scale the foreground image
        fg_image = pygame.image.load('assets/graphics/environment/ground.png').convert_alpha()
        self.image = pygame.transform.scale(fg_image, pygame.math.Vector2(fg_image.get_size()) * scale_factor)
        
        # position
        self.rect = self.image.get_rect(bottomleft = (0, SCREEN_HEIGHT))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # collision mask
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.pos.x -= 360 * dt
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)

class Player(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)

        # image
        self.import_frames(scale_factor)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
    
        # rect
        self.rect = self.image.get_rect(midleft=(SCREEN_WIDTH / 6, SCREEN_HEIGHT / 2))
        self.pos = pygame.math.Vector2(self.rect.topleft)

        # collision mask
        self.mask = pygame.mask.from_surface(self.image)

        # movement
        self.gravity = 600
        self.direction = 0

        # sound
        self.jump_sound = pygame.mixer.Sound('assets/sounds/jump.wav')
        self.jump_sound.set_volume(.2)

    def import_frames(self, scale_factor):
        self.frames = []
        # import, scale and append all the frames to frames
        for i in range(3):
            srf = pygame.image.load(f'assets/graphics/plane/red{i}.png').convert_alpha()
            self.frames.append(pygame.transform.scale(srf, pygame.math.Vector2(srf.get_size()) * scale_factor))

    def apply_gravity(self, dt):
        self.direction += self.gravity * dt
        self.pos.y += self.direction * dt
        self.rect.y = self.pos.y

    def jump(self):
        self.jump_sound.play()
        self.direction = -400

    def animate(self, dt):
        self.frame_index += 10 * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

    def rotate(self):
        rotated_plane = pygame.transform.rotozoom(self.image, -self.direction * .08, 1)
        self.image = rotated_plane
        # collision mask
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.apply_gravity(dt)
        self.animate(dt)
        self.rotate()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, groups, scale_factor):
        super().__init__(groups)
        self.sprite_type = 'obstacle'
        orientation = random.choice(['up', 'down'])
        srf = pygame.image.load(f'assets/graphics/obstacles/{random.choice([0, 1])}.png').convert_alpha()
        self.image = pygame.transform.scale(srf, pygame.math.Vector2(srf.get_size()) * scale_factor)
        
        # collision mask
        self.mask = pygame.mask.from_surface(self.image)

        x = SCREEN_WIDTH + random.randint(40, 80)

        if orientation == 'up':
            y = SCREEN_HEIGHT + random.randint(10, 50)
            self.rect = self.image.get_rect(midbottom=(x, y))
        else:
            y = random.randint(-50, -10)
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect(midtop=(x, y))

        self.pos = pygame.math.Vector2(self.rect.topleft)

    def update(self, dt):
        self.pos.x -= 200 * dt
        self.rect.x = round(self.pos.x)
        if self.rect.right <= -100:
            self.kill()

