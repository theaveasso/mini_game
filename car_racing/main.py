import math
import time
import pygame

from car import PlayerCar

# loading game assets
GRASS = pygame.image.load('assets/grass.jpg')
TRACK = pygame.image.load('assets/track.png')
FINISH = pygame.image.load('assets/finish.png')
BORDER = pygame.image.load('assets/track-border.png')

# game variable
FPS = 60
SCREEN_WIDTH, SCREEN_HEIGHT = TRACK.get_width(), TRACK.get_height()
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Car Racing Game')
clock = pygame.time.Clock()

    
def draw(screen, images, player_car):
    for img, pos in images:
        screen.blit(img, pos)
        
    pygame.display.update()
    
def main():
    player_car = PlayerCar()
    
    RUN = True
    # game asset
    assets = [(GRASS, (0, 0)), (TRACK, (0, 0)), (BORDER, (0, 0)),
              (FINISH, (130, 130))]

    
    while RUN:
        clock.tick(FPS)
        dt = clock.get_time() / 1000
        draw(screen, assets, player_car)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False
                break
        
        KEYS = pygame.key.get_pressed()
        if KEYS[pygame.K_UP]:
            if player_car.velocity.y < 0:
                player_car.acceleration = player_car.brake_deceleration
            else:
                player_car.acceleration += 1 * dt
            print(player_car.position)
        elif KEYS[pygame.K_DOWN]:
            if player_car.velocity.y > 0:
                player_car.acceleration -= player_car.brake_deceleration
            else:
                player_car.acceleration -= 1 * dt
        elif KEYS[pygame.K_SPACE]:
            if abs(player_car.velocity.y) > dt * player_car.brake_deceleration:
                player_car.acceleration = -math.copysign(player_car.brake_deceleration, player_car.velocity.y)
            else:
                player_car = -player_car.velocity.y / dt
        else:
            if abs(player_car.velocity.y) > dt * player_car.free_deceleration:
                player_car.acceleration = -math.copysign(player_car.free_deceleration, player_car.velocity.y)
            else:
                if dt != 0:
                    player_car.acceleration = -player_car.velocity.y / dt
            
        player_car.acceleration = max(-player_car.max_acceleration, min(player_car.acceleration, player_car.max_acceleration))
        
        if KEYS[pygame.K_RIGHT]:
            player_car.sterring -= 30 * dt
        elif KEYS[pygame.K_LEFT]:
            player_car.sterring += 30 * dt
        else:
            player_car.sterring = 0
        
        player_car.sterring = max(-player_car.max_steering, min(player_car.sterring, player_car.max_steering))
        
        player_car.update(dt)
        
        player_car.draw(screen)
        pygame.display.flip()
        
    pygame.quit()
    
if __name__ == '__main__':
    main()
            
