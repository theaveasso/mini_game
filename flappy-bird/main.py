import sys
import time
import pygame

from sprites import BG, FG, Player, Obstacle

class Game:
    def __init__(self):
        pygame.init()
        self.active = True
        self.clock = pygame.time.Clock()
        screen_width, screen_height = 480, 800
        pygame.display.set_caption('Flappy Bird')
        self.screen = pygame.display.set_mode((screen_width, screen_height))

        # sprites
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # scale factor
        bg_height = pygame.image.load('assets/graphics/environment/background.png').get_height()
        self.scale_factor = screen_height / bg_height

        # sprites setup
        BG(self.all_sprites, self.scale_factor)
        FG([self.all_sprites, self.collision_sprites], self.scale_factor / 2)
        self.plane = Player(self.all_sprites, self.scale_factor/ 2)

        # timer
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1400)

        # text
        self.font = pygame.font.Font('assets/graphics/font/BD_Cartoon_Shout.ttf', 30)
        self.score = 0
        self.start_offset = 0

        # menu
        self.menu_srf = pygame.image.load('assets/graphics/ui/menu.png').convert_alpha()
        self.menu_rec = self.menu_srf.get_rect(center=(480/2, 800/2))

        # sound
        self.sfx = pygame.mixer.Sound('assets/sounds/music.wav')
        self.sfx.set_volume(.5)
        self.sfx.play(loops=-1)

    def display_score(self):
        if self.active:
            self.score = (pygame.time.get_ticks() - self.start_offset) // 1400
            y = 800 / 10
        else:
            y = 800 / 2 + (self.menu_rec.height / 1.5)

        score_srf = self.font.render(str(self.score), True, 'black', )
        score_rect = score_srf.get_rect(midtop=(480/2, y))
        self.screen.blit(score_srf, score_rect)

    def collision(self):
        if pygame.sprite.spritecollide(self.plane, self.collision_sprites, False, pygame.sprite.collide_mask) or self.plane.rect.top <= 0:
            for sprite in self.collision_sprites:
                if sprite.sprite_type == 'obstacle':
                    sprite.kill()
            self.plane.kill()
            self.active = False

    def run(self):
        last_time = time.time()
        
        while True:
            # evnet loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.active:
                        self.plane.jump()
                    else:
                        self.active = True
                        self.start_offset = pygame.time.get_ticks()
                        self.plane = Player(self.all_sprites, self.scale_factor/ 2)

                if event.type == self.obstacle_timer and self.active:
                    Obstacle([self.all_sprites, self.collision_sprites], self.scale_factor * 1.1)

            # delta time
            dt = time.time() - last_time
            last_time = time.time()

            # game logic
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.screen)
            self.display_score()
            
            # check collision to end the game
            if self.active:
                self.collision()
            else:
                self.screen.blit(self.menu_srf, self.menu_rec)

            self.clock.tick(120)

            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()