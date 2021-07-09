import sys, pygame, random
import time

pygame.init()
pygame.mixer.init()

size = width, height = 706, 540
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Planet Express Delivery")
background_image = pygame.image.load("./background.jpg").convert()
text_font = pygame.font.Font("./Futurama Bold Font.ttf", 12)

background_music = pygame.mixer.music.load("./theme_song.mp3")
pygame.mixer.music.play(-1)

# start time for timer and a best time tracker
start_time = time.time()

def get_best_time():
    with open("best_time.txt", "r") as file:
        return file.read()

try:
    best_time = float(get_best_time())
except:    
    best_time = 0

# bool to keep track of played or paused
paused = False

# pause/play buttons
play_button_image = pygame.image.load("./play_button.png")
play_button_image = pygame.transform.scale(play_button_image, (40, 40))
play_button_rect = play_button_image.get_rect(center = (675, 30))
pause_button_image = pygame.image.load("./pause_button.png")
pause_button_image = pygame.transform.scale(pause_button_image, (40, 40))
pause_button_rect = pause_button_image.get_rect(center = (675, 30))

SHIP_VELOCITY = 10
SHIP_LASER_COOLDOWN_SPEED = 450
ALIEN_LASER_COOLDOWN_SPEED = 750
ALIEN_SPAWN_SPEED = 1000
MAX_NUM_ALIENS = 5

# create event for shooting lasers
ship_laser_shot_event = pygame.USEREVENT + 1
alien_laser_shot_event = pygame.USEREVENT + 2
alien_spawn_event = pygame.USEREVENT + 3
ship_laser_cooldown_finished = True
alien_laser_cooldown_finished = True

pygame.time.set_timer(alien_laser_shot_event, ALIEN_LASER_COOLDOWN_SPEED)
pygame.time.set_timer(alien_spawn_event, ALIEN_SPAWN_SPEED)

class PlanetExpressShip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("./planet_express_ship.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(center = (155, 180))

        self.health = 10
        self.health_images = [pygame.image.load("./heart0.png"), pygame.image.load("./heart0.5.png"), pygame.image.load("./heart1.png"), pygame.image.load("./heart1.5.png"), 
        pygame.image.load("./heart2.png"), pygame.image.load("./heart2.5.png"), pygame.image.load("./heart3.png"), pygame.image.load("./heart3.5.png"), 
        pygame.image.load("./heart4.png"), pygame.image.load("./heart4.5.png"), pygame.image.load("./heart5.png")]
        self.health_image = self.health_images[self.health]
        self.health_image = pygame.transform.scale(self.health_image, (75, 15))

        self.ammo = 5
        self.ammo_image = pygame.image.load("./ammo.png")
        self.ammo_image = pygame.transform.scale(self.ammo_image, (40, 23))
        self.ammo_rect = self.ammo_image.get_rect(center = (random.uniform(10, width - 140), random.uniform(10, height - 10)))


    def update_healthbar_position(self, x, y):
        self.health_rect = self.health_image.get_rect(center = (x + 59, y + 85))

    def update_health(self):
        self.health -= 1
        self.health_image = self.health_images[self.health]
        self.health_image = pygame.transform.scale(self.health_image, (75, 15))     

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
        self.rect.x += 15
        # If we are past the right boundary, kill self
        if self.rect.x > width:
            self.kill()

class Alien(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("./aliens.png")
        self.image = pygame.transform.scale(self.image, (130, 90))
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(center = (width + 10, random.uniform(15, height - 15)))
        self.move_up = bool(random.getrandbits(1))
        # self.healthbar = 

    def update(self):
        if self.rect.x > width - 130:
            self.rect.x -= 3
        else:
            if self.move_up:
                self.rect.y -= 2
                self.move_up = not self.move_up
            elif self.move_up == False:
                self.rect.y += 2
                self.move_up = not self.move_up

    def create_laser(self):
        return AlienLaser(self.rect.x + 50, self.rect.y + 50)            

class AlienLaser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("./red_laser.png")
        self.image = pygame.transform.scale(self.image, (70, 110))
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect(center = (x, y))
        self.speed = random.uniform(5, 20)

    def update(self):
        # update x position
        self.rect.x -= self.speed
        # If we are past the left boundary, kill self
        if self.rect.x < 0:
            self.kill()

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

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.should_animate = False
        self.explosion_sprites = []
        self.explosion_sprites.append(pygame.image.load("explosion0.png"))
        self.explosion_sprites.append(pygame.image.load("explosion1.png"))
        self.explosion_sprites.append(pygame.image.load("explosion2.png"))
        self.explosion_sprites.append(pygame.image.load("explosion3.png"))
        self.explosion_sprites.append(pygame.image.load("explosion4.png"))
        self.explosion_sprites.append(pygame.image.load("explosion5.png"))
        self.explosion_sprites.append(pygame.image.load("explosion6.png"))
        self.explosion_sprites.append(pygame.image.load("explosion7.png"))
        
        self.curr_sprite = 0
        self.image = self.explosion_sprites[self.curr_sprite]
        self.rect = self.image.get_rect(center = (x, y))

    def animate(self):
        self.should_animate = True    

    def update(self, animation_speed):
        if self.should_animate == True:
            self.curr_sprite += animation_speed

            if self.curr_sprite >= len(self.explosion_sprites):
                self.curr_sprite = 0
                self.should_animate = False  

            self.image = self.explosion_sprites[self.curr_sprite]  

ship = PlanetExpressShip()
ship_sprite = pygame.sprite.Group()
ship_sprite.add(ship)
ship_laser_sprite = pygame.sprite.Group()

alien_sprite = pygame.sprite.Group()
alien_laser_sprite = pygame.sprite.Group()
num_aliens = 0
aliens = []

asteroid_sprite = pygame.sprite.Group()

explosion = Explosion(50, 50)

clock = pygame.time.Clock()
while 1:
    if not paused:
        clock.tick(60)
        screen.fill((0, 0, 0))
        screen.blit(background_image, [0, 0])
        ship.update_healthbar_position(ship.rect.x, ship.rect.y)
        screen.blit(ship.health_image, ship.health_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pos() >= (664, 16) and pygame.mouse.get_pos() <= (685, 34):
                    paused = True  
            elif event.type == ship_laser_shot_event:
                # when the timeout of LASER_COOLDOWN_SPEED is over, reset it
                ship_laser_cooldown_finished = True
                pygame.time.set_timer(ship_laser_shot_event, 0)
            elif event.type == alien_laser_shot_event:
                for enemy in aliens:
                    alien_laser_sprite.add(enemy.create_laser())
            elif event.type == alien_spawn_event and num_aliens < MAX_NUM_ALIENS:
                alien = Alien()
                aliens.append(alien)
                alien_sprite.add(alien)
                num_aliens += 1

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
            if ship_laser_cooldown_finished and ship.ammo > 0:
                ship_laser_sprite.add(ship.create_laser())
                ship.ammo -= 1
                ship_laser_cooldown_finished = False
                # timeout of LASER_COOLDOWN_SPEED
                pygame.time.set_timer(ship_laser_shot_event, SHIP_LASER_COOLDOWN_SPEED)

        if ship.ammo == 0:
            screen.blit(ship.ammo_image, ship.ammo_rect)                          
           
        ship_laser_sprite.draw(screen)
        ship_laser_sprite.update()
        alien_laser_sprite.draw(screen)
        alien_laser_sprite.update()
        ship_sprite.draw(screen)
        alien_sprite.draw(screen)
        alien_sprite.update()

        # check for collisions
        collision = pygame.sprite.groupcollide(alien_laser_sprite, ship_sprite, True, False, collided=pygame.sprite.collide_rect_ratio(0.3))
        
        # if collision != None:
        #     ship.update_health()
        #     print(ship.health)

        screen.blit(pause_button_image, pause_button_rect)

        pygame.mixer.music.unpause()

        elapsed_time = time.time() - start_time

        if best_time < elapsed_time:
            best_time = elapsed_time
        with open("best_time.txt", "w") as file:
            file.write(str(best_time))        

        elapsed_time_text = text_font.render('ELAPSED TIME: %.2f' % (elapsed_time), True, (234, 100, 89))
        best_time_text = text_font.render('BEST TIME: %.2f' % (best_time), True, (238, 118, 0))
        ammo_left_text = text_font.render('LASERS REMAINING: ' + str(ship.ammo), True, (161, 95, 169))
        screen.blit(elapsed_time_text, (10, 10))
        screen.blit(best_time_text, (10, 30))
        screen.blit(ammo_left_text, (10, 50))

        pygame.display.flip()
    else:
        start_time = time.time() - elapsed_time
        screen.blit(play_button_image, play_button_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pos() >= (664, 16) and pygame.mouse.get_pos() <= (685, 34):
                    paused = False

        pygame.mixer.music.pause()

        pygame.display.flip()              