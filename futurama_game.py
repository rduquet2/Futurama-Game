import sys, pygame, random

pygame.init()

size = width, height = 706, 540
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Planet Express Delivery")
background_image = pygame.image.load("./background.jpg").convert()

# buttons
play_button_image = pygame.image.load("./play_button.png")
play_button_image = pygame.transform.scale(play_button_image, (40, 40))
play_button_rect = play_button_image.get_rect(center = (675, 30))
pause_button_image = pygame.image.load("./pause_button.png")
pause_button_image = pygame.transform.scale(pause_button_image, (40, 40))
pause_button_rect = pause_button_image.get_rect(center = (675, 30))

SHIP_VELOCITY = 6
SHIP_LASER_COOLDOWN_SPEED = 450
ALIEN_LASER_COOLDOWN_SPEED = 1000

# create event for shooting lasers
ship_laser_shot_event = pygame.USEREVENT + 1
alien_laser_shot_event = pygame.USEREVENT + 2
ship_laser_cooldown_finished = True
alien_laser_cooldown_finished = True

class PlanetExpressShip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("./planet_express_ship.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(center = (155, 180))

    def create_laser(self):
        return PlanetExpressShipLaser(self.rect.x + 70, self.rect.y + 35)    

class PlanetExpressShipLaser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("./purple_laser.png")
        self.image = pygame.transform.scale(self.image, (70, 110))
        self.rect = self.image.get_rect(center = (x, y))

    def update(self):
        # update x position
        self.rect.x += 5
        # If we are past the right boundary, kill self
        if self.rect.x > width:
            self.kill()

class Alien(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image.load("/.aliens.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(center = (width + 10, random.uniform(0, height)))

    # def update(self):


class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("./asteroid.png")
        self.image = pygame.transform.scale(self.image, (75, 75))
        # generate asteroid in right boundary randomly
        self.rect = self.image.get_rect(center = (width + 10, random.uniform(0, height)))
        self.x_speed = random.uniform(-10, -5)
        self.y_speed = random.uniform(-10, 10)

    def update(self):
        self.rect = self.rect.move(self.x_speed, self.y_speed)

        if self.rect.bottom > height or self.rect.top < 0:
            self.y_speed = self.y_speed * -1

        if self.rect.right < 0:
            self.kill()

ship = PlanetExpressShip()
ship_sprite = pygame.sprite.Group()
ship_sprite.add(ship)

ship_laser_sprite = pygame.sprite.Group()
asteroid_sprite = pygame.sprite.Group()

# states to keep track of played or paused
button_image = pause_button_image
button_rect = pause_button_rect
paused = False

clock = pygame.time.Clock()
while 1:
    clock.tick(60)
    screen.fill((0, 0, 0))
    screen.blit(background_image, [0, 0])
    screen.blit(button_image, button_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pos() >= (664, 16) and pygame.mouse.get_pos() <= (685, 34):
                paused = not paused
                if paused == False:
                    button_image = pause_button_image
                    button_rect = pause_button_rect
                else:
                    button_image = play_button_image
                    button_rect = play_button_rect  
        elif event.type == ship_laser_shot_event:
            # when the timeout of LASER_COOLDOWN_SPEED is over, reset it
            ship_laser_cooldown_finished = True
            pygame.time.set_timer(ship_laser_shot_event, 0)    

    # handle WASD or arrow key movement
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        ship.rect.x -= SHIP_VELOCITY
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        ship.rect.x += SHIP_VELOCITY
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        ship.rect.y -= SHIP_VELOCITY
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        ship.rect.y += SHIP_VELOCITY           

    # handle border collisions    
    if ship.rect.left < 0:
        ship.rect.left = 0
    if ship.rect.right > width:
        ship.rect.right = width
    if ship.rect.top < 0:
        ship.rect.top = 0
    if ship.rect.bottom > height:
        ship.rect.bottom = height

    if keys[pygame.K_SPACE]:
        if ship_laser_cooldown_finished:
            ship_laser_sprite.add(ship.create_laser())
            ship_laser_cooldown_finished = False
            # timeout of LASER_COOLDOWN_SPEED
            pygame.time.set_timer(ship_laser_shot_event, SHIP_LASER_COOLDOWN_SPEED)                
        
    ship_laser_sprite.draw(screen)
    ship_laser_sprite.update()
    ship_sprite.draw(screen)

    pygame.display.flip()