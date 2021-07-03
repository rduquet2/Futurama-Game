import sys, pygame, random

pygame.init()

size = width, height = 750, 750
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Planet Express Delivery")
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
        self.rect = self.image.get_rect(center = (350, 350))

    def create_laser(self):
        return PlanetExpressShipLaser(self.rect.x + 70, self.rect.y + 35)    

class PlanetExpressShipLaser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load("./purple_laser.png")
        self.image = pygame.transform.scale(self.image, (70, 110))
        self.rect = self.image.get_rect(center = (x, y))

    def update(self):
        # update x position
        self.rect.x += 5
        # If we are past the right boundary, kill self
        if self.rect.x >= width:
            self.kill()

class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(self)

        self.image = pygame.image.load("./asteroid.png")
        self.image = pygame.transform.scale(self.image, (5, 5))
        self.rect = self.image.get_rect(center = (width + 10, random.uniform()))


ship = PlanetExpressShip()
ship_sprite = pygame.sprite.Group()
ship_sprite.add(ship)

ship_laser_sprite = pygame.sprite.Group()

clock = pygame.time.Clock()
while 1:
    clock.tick(60)
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
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