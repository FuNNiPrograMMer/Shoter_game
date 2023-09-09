#from
from pygame import *
from random import randint


#переменные
game = True
finish = True
skore = 0
lost = 0
pause = True
stop = False
num_fire = 0
real_time = False
enemy_image = ['enemy.png', 'enemy2.png', 'enemy3.png', 'enemy4.png', 'enemy5.png',]


#класс спрайты
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, playerw, playerh):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (playerw, playerh))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 920:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, -15, 25, 35)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y+= self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(0, win_width-80)
            self.rect.y = 0
            lost = lost+1


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


class Coin(GameSprite):
    def update(self):
        self.rect.y+= self.speed
        global skore
        if self.rect.y > win_height:
            self.rect.x = randint(0, win_width-80)
            self.rect.y = 0
        if sprite.collide_rect(player, coin):
            skore+=5
            coin_drop.play()
            self.rect.x = randint(0, win_width-80)
            self.rect.y = 0


#окошко
win_width = 1000
win_height = 600
window = display.set_mode((win_width, win_height))
display.set_caption("Galaga")
background = transform.scale(image.load('space.jpg'), (win_width, win_height))


#музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
theme = mixer.Sound('theme.wav')
theme.play()
fire_sound = mixer.Sound('fire.wav')
die = mixer.Sound('die.wav')
boom = mixer.Sound('boom.wav')
coin_drop = mixer.Sound('coin.wav')
win_m = mixer.Sound('win.wav')


#текст
font.init()
font = font.Font(None, 50)
#text = font.Font(None, 300)
lose = font.render('Game over!', True,(255, 0, 0))
win = font.render('You win!', True,(0, 255, 0))


#экземпляры
monsters = sprite.Group()
bullets = sprite.Group()
player = Player('galaga.png', 460, 500, 30, 80, 100)
for i in range(5):
    enemy = Enemy(enemy_image[randint(0,4)], randint(0, win_width-80), 0, randint(1, 30), 80, 80)
    monsters.add(enemy)
logo = GameSprite('logo.png', 800, 0, 0, 200, 100)
coin = Coin('coin.png', randint(0, win_width-80), 0, 80, 75, 75)


#цикл
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    keys_pressed = key.get_pressed()

    if keys_pressed[K_w]:
        if num_fire < 10 and real_time == False:
            num_fire+=1
            player.fire()
            fire_sound.play()

    if keys_pressed[K_SPACE] and finish == True and pause != True and stop == True:
        finish = False
        stop = False
        skore = 0
        lost = 0
        continue

    if keys_pressed[K_SPACE] and finish == True and pause == True and stop != True:
        finish = False
        pause = False
        continue

    if keys_pressed[K_SPACE] and finish == True and pause == True and stop == True:
        finish = False
        pause = False
        skore = 0
        lost = 0
        continue

    sprites_list = sprite.groupcollide(monsters, bullets, True, True)
    for s in sprites_list:
        skore+=1
        enemy = Enemy(enemy_image[randint(0,4)], randint(0, win_width-80), 0, 15, 80, 80)
        monsters.add(enemy)

    if not finish:
        window.blit(background, (0, 0))
        chet = font.render('Cчёт:'+str(skore), True, (255, 255, 255))
        window.blit(chet, (20, 20))
        prop = font.render('пропущено:'+str(lost), True, (255, 255, 255))
        window.blit(prop, (20, 60))
        upr = font.render('"A"-Игрок на лево', True, (0, 246, 255))
        upr1 = font.render('"D"-Игрок на право', True, (0, 246, 255))
        upr2 = font.render('"W"-Выстрел', True, (0, 246, 255))
        upr3 = font.render('"Пробел"-Сброс', True, (0, 246, 255))

        window.blit(upr, (670, 400))
        window.blit(upr1, (670, 450))
        window.blit(upr2, (670, 500))
        window.blit(upr3, (670, 550))

        player.update()
        coin.update()
        bullets.update()
        monsters.update()

        player.reset()
        logo.reset()
        coin.reset()
        
        bullets.draw(window)
        monsters.draw(window)
        
        display.update()
    

    if keys_pressed[K_ESCAPE]:
        finish = True
        pause = True

    if sprite.spritecollide(player, monsters, False):
        window.blit(lose, (400,250))

        if finish != True:
            boom.play()
        finish = True
        stop = True

    if skore >= 100:
        if finish!=True:
            win_m.play()
        finish = True
        window.blit(win, (400,250))
        stop = True

    if lost >= 50:
        if finish != True:
            die.play()
        finish = True
        stop = True
        window.blit(lose, (400,250))


    #концовка
    display.update()
    time.delay(60)
