#Create your own shooter
from pygame import * 
from random import randint
from time import time  as timer

win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption('shooter game')
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 70)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_x = 65, size_y = 65):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys [K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top,15, 10, 20)
        bullets.add(bullet)
missed = 0       
Score = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global missed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(0,640)
            self.speed= randint(1,3)
            missed += 1
            text_lose = font1.render("Missed:" + str(missed), 1, (255, 255, 255))
class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(0,640)
            self.speed= randint(1,3)



            
text_lose = font1.render("Missed:" + str(missed), 1, (255, 255, 255))
text_Win = font1.render("Score:" + str(Score), 1, (255, 255, 255))
idiot = sprite.Group()
dumb = sprite.Group()
bullets = sprite.Group()
for i in range(5): 
    ufo = Enemy("rocket.png", randint(0,640), 0 , 3)
    
    idiot.add(ufo)
    
for i in range(2):
    asteroid = Asteroid("asteroid.png", randint(0,640), 0, 5)
    dumb.add(asteroid)

rocket = Player("ufo.png",5,450, 5)
game = True
clock = time.Clock()
fps = 60
finish = False
num_fire = 0
rel_time = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    rocket.fire()
                    num_fire += 1
                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    cur_time = timer()
                    
                
    if finish == False:
        window.blit(background,(0, 0))
        text_lose = font1.render("Missed:" + str(missed), 1, (255, 255, 255))
        text_Win = font1.render("Score:" + str(Score), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        window.blit(text_Win, (10, 10))
        rocket.update()
        
        if sprite.spritecollide(
            rocket, idiot, False
        ):
            finish = True
            lose = font2.render(
                'YOU LOSE!', True, (255, 215, 0)
            )
            window.blit(lose, (200,200))
        if sprite.spritecollide(
            rocket, dumb, False
        ):
            finish = True
            lose = font2.render(
                'YOU LOSE!', True, (255, 215, 0)
            )
            window.blit(lose, (200,200))
        sprite_list = sprite.groupcollide(
            idiot, bullets, True, True
        )
        for i in sprite_list:
            Score += 1
            ufo = Enemy("rocket.png", randint(0,640), 0 , 3)
            idiot.add(ufo)
            
        Victory = font2.render(
                'VICTORY', True, (255, 215, 0)
            )    
        if Score >= 10:
            window.blit(Victory, (200,200))
            finish = True
        if missed >= 15:
            lose = font2.render(
                'YOU LOSE!', True, (255, 215, 0)
            )
            window.blit(lose, (200,200))
            finish = True
        rocket.reset()
        idiot.draw(window)
        idiot.update()
        dumb.draw(window)
        dumb.update()
        bullets.update()
        bullets.draw(window)
        if rel_time == True:
            cur_time2 = timer()
            if cur_time2 - cur_time < 3:
                Reload = font2.render('Wait', 1, (255, 215, 0))
                window.blit(Reload, (200,200))                
            else: 
                rel_time = False
                num_fire = 0
        display.update()
        clock.tick(fps)

    

    

    