#Створи власний Шутер!

from typing import Any
from pygame import *

from random import randint


# фонова музика
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')


font.init()
font1 = font.Font(None,36)
#win = font1.render('1', (255,255,255))
#lose = font1.render('2', (255,255,255))
# нам потрібні такі картинки:
img_back = "galaxy.jpg"  # фон гри
img_hero = "rocket.png"  # герой
img_enemy = "ufo.png"
img_bullet = "bullet.png"

score = 0
lost = 0
max_lost = 3








# клас-батько для інших спрайтів
class GameSprite(sprite.Sprite):
    # конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # викликаємо конструктор класу (Sprite):
        sprite.Sprite.__init__(self)
        # кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(
            image.load(player_image), (size_x, size_y))
        self.speed = player_speed


        # кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y


    # метод, що малює героя на вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


# клас головного гравця
class Player(GameSprite):


    # метод для керування спрайтом стрілками клавіатури
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed


    # метод "постріл" (використовуємо місце гравця, щоб створити там кулю)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80,win_width-80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()



# створюємо віконце
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))


# створюємо спрайти
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
monsters = sprite.Group()

for i in range(1,6):
    monster = Enemy(img_enemy, randint(80,win_width-80), -40, 80,50,randint(1,5))
    monsters.add(monster)

bullets = sprite.Group()

# змінна "гра закінчилася": як тільки вона стає True, в основному циклі перестають працювати спрайти
finish = False


# Основний цикл гри:
run = True  # прапорець скидається кнопкою закриття вікна


while run:
    # подія натискання на кнопку Закрити
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()


    if not finish:
        # оновлюємо фон
        window.blit(background, (0, 0))
        text = font1.render('рахунок' + str(score), 1, (255,255,255))
        window.blit(text, (10,50))

        text_lost = font1.render('Пропущено' + str(lost), 1, (255,255,255))
        window.blit(text_lost, (10,90))
        # рухи спрайтів
        ship.update()
        monsters.update()
        bullets.update()

        # оновлюємо їх у новому місці при кожній ітерації циклу
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        display.update()
    # цикл спрацьовує кожні 0.05 секунд
    time.delay(50)
