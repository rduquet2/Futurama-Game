import sys, pygame, random

pygame.init()

size = width, height = 750, 750
screen = pygame.display.set_mode(size)
velocity = 6

class PlanetExpressShip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("./planet_express_ship.png")
        self.image = pygame.transform.scale(self.image, (100, 100))

        self.rect = self.image.get_rect()
        self.rect.center = (350, 350)

ship = PlanetExpressShip()
ship_sprite = pygame.sprite.Group()
ship_sprite.add(ship)

clock = pygame.time.Clock()
while 1:
    clock.tick(60)
    screen.fill((0, 0, 0))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        ship.rect.x -= velocity
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        ship.rect.x += velocity
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        ship.rect.y -= velocity
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        ship.rect.y += velocity            

    ship_sprite.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()     
    pygame.display.flip()