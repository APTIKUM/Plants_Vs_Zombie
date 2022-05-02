import sys

from pygame import *
import time as timing
from random import *
from module_music import *
from sys import *

init()

window_width = 1024
window_height = 720


# создание ячеек
def maker_cells():
    global cell_sprite
    total_cell = 45
    x = 120
    y = 110
    for i in range(total_cell):
        cell = cells('image/background_cell.png', x, y, 95, 95)
        cell_sprite.add(cell)
        x += 95
        if (i + 1) % 9 == 0:
            y += 115
            x = 120


def maker_lawn_mower():
    global lawn_mower_sprite
    total_lawn_mower = 5
    x = 30
    y = 130
    for i in range(total_lawn_mower):
        lawn_mower = Lawn_mowers('image/Lawn_mower/Lawn_Mower.png', x, y, 90, 75)
        lawn_mower_sprite.add(lawn_mower)
        y += 115

def event_exit():
    for e in event.get():
        if e.type == QUIT:
            sys.exit()
zombies_y_list = [115, 230, 345, 460, 575]

use_plants_take = False
type_plant = 'True'
flag_game = True
backmusic()
window_set_mode = (window_width, window_height)
display.set_caption('Plants vs Zombie')
window = display.set_mode(window_set_mode)
window_background = transform.scale(image.load('image/background.jpg'), window_set_mode)
window.blit(window_background, (0, 0))
time_for_creat_sun = timing.time()
dead_zombie = 0
zombie_end = False
shovel_push = False

playing = 0
# фигня функцтия что бы всё делалось
def gameplay():
    window.blit(window_background, (0, 0))
    money_label.set_text(str(money_sun), 40, (0, 0, 0))
    real_sun()
    #cell_sprite.update()
    cards_sprite.draw(window)
    cards_sprite.update()
    plants_sprite.update()
    plants_sprite.draw(window)
    cancell_plants.reset()
    shovel_cards.reset()
    zombie_sprite.update()
    zombie_sprite.draw(window)
    bullets_sprite.update()
    bullets_sprite.draw(window)
    zombie_fire_sprite.draw(window)
    lawn_mower_sprite.update()
    lawn_mower_sprite.draw(window)
    FIRE_sprite.update()
    FIRE_sprite.draw(window)
    zombie_dead_sprite.update()
    zombie_dead_sprite.draw(window)
    sun_sprite.update()
    sun_sprite.draw(window)
    shovel_blit(shovel_push)


# класс для ВСЕГО
class GameSprite(sprite.Sprite):
    def __init__(self, picture, x, y, width, height):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(picture), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

    def set_text(self, text, fsize, text_color):
        text_space = ''
        if len(text) == 2:
            text_space = '  '
        elif len(text) == 3:
            text_space = ' '
        elif len(text) == 1:
            text_space = '   '
        self.image = font.Font(None, fsize).render(text_space + text, True, text_color)
        window.blit(self.image, (self.rect.x, self.rect.y))

    def collede_mouse(self, x_mouse, y_mouse):
        return self.rect.collidepoint(x_mouse, y_mouse)


# класс для ячейки на которые стафишь
class cells(GameSprite):
    def __init__(self, picture, x, y, width, height):
        super().__init__(picture, x, y, width, height)
        self.use = True

    def update(self):
        if self.use:
            self.reset()

    def collede_cells_mouse(self, x_mouse, y_mouse):
        global click_on_cell
        if self.rect.collidepoint(x_mouse, y_mouse) and self.use:
            click_on_cell = False
            self.use = False
            return self.rect.x, self.rect.y


# класс для солнышек которые ты собираешь
class suns(GameSprite):
    def __init__(self, picture, x, y, width, height, down_y):
        super().__init__(picture, x, y, width, height)
        self.time_sun = timing.time()
        self.down_y = down_y
        self.collect = False
        self.move_down = 2
        self.move_dead_x = 100
        self.move_dead_y = 30
        self.image_list = 0

    def collected(self):
        global money_sun, suns_image_list
        if self.collect:
            if self.rect.x > 15:
                self.rect.x -= self.move_dead_x
            if self.rect.y > 30:
                self.rect.y -= self.move_dead_y
                if self.rect.x < 100:
                    self.rect.y -= 20
            self.image = transform.scale(image.load(suns_image_list[self.image_list]),
                                         (self.rect.width, self.rect.height))
            if self.image_list != 4:
                self.image_list += 1
            if sprite.groupcollide(sun_sprite, suns_end, True, False):
                money_sun += 25

    def update(self):
        if self.rect.y < self.down_y:
            self.rect.y += self.move_down
        time_dead_sun = timing.time()
        if time_dead_sun - self.time_sun > 8:
            self.kill()

    def collede_sun_mouse(self, x_mouse, y_mouse):
        global money_sun
        if self.rect.collidepoint(x_mouse, y_mouse):
            sound_sun()
            self.collect = True
            self.move_down = 0


# впомогательная фигня что бы первое солнце делалось не через 10 а через 3 секунды
first_time_created_sun = True


# функция что бы солнышки создавались без подсолнуха обычные с неба 1
def real_sun():
    global time_for_creat_sun, sun_sprite, first_time_created_sun
    time_for_creat_sun_2 = timing.time()
    if time_for_creat_sun_2 - time_for_creat_sun >= 10 or (
            first_time_created_sun and time_for_creat_sun_2 - time_for_creat_sun >= 3) and len(sun_sprite) < 4:
        first_time_created_sun = False
        sun = suns('image/suns/sun_0.png', randint(100, window_width - 200), randint(50, window_height - 500), 90, 90,
                   randint(200, window_height - 400))
        sun_sprite.add(sun)
        time_for_creat_sun = timing.time()


class cards_sprite_class(GameSprite):
    def __init__(self, picture, x, y, width, height, cost, time_reset, type_plant):
        super().__init__(picture, x, y, width, height)
        self.cost = cost
        self.time_reset = time_reset
        self.time_card_start = timing.time()
        self.time_card_end = 0
        self.first_time = True
        self.type_plant = type_plant

    def update(self):  # затемнение карточек если мало бабла или кулдаун (АсуждАю) или ты уже выбрал карточку
        global money_sun
        self.time_card_end = timing.time()
        # if click_on_cell:
        #   window.blit(transform.scale(image.load('image/cards/image_card_black_use.png'), (self.rect.width, self.rect.height)), (self.rect.x, self.rect.y))
        if self.time_card_end - self.time_card_start < self.time_reset and not self.first_time:
            window.blit(transform.scale(image.load('image/cards/image_card_black_time.png'),
                                        (self.rect.width, self.rect.height)), (self.rect.x, self.rect.y))
        elif self.cost > money_sun:
            window.blit(transform.scale(image.load('image/cards/image_card_black_money.png'),
                                        (self.rect.width, self.rect.height)), (self.rect.x, self.rect.y))

    def collede_cards_mouse(self, x_mouse, y_mouse):
        global money_sun, click_on_cell, type_plant, price_for_cancell
        if self.rect.collidepoint(x_mouse, y_mouse):
            self.time_card_end = timing.time()
            if not click_on_cell:
                if money_sun >= self.cost:
                    if self.time_card_end - self.time_card_start >= self.time_reset or self.first_time:
                        click_on_cell = True
                        self.time_card_start = self.time_card_end
                        self.time_card_end = 0
                        type_plant = self.type_plant
                        self.first_time = False
                        plants_pay(True)
                        price_for_cancell = self.cost
                        money_sun -= self.cost
                    else:
                        plants_pay(False)
                else:
                    plants_pay(False)
                    money_label.set_text(str(money_sun), 40, (255, 0, 0))
            else:
                plants_pay(False)


class Zombie(GameSprite):
    def __init__(self, picture, x, y, width, height, amount_animation, health, image_file, speed, dead_head):
        super().__init__(picture, x, y, width, height)
        self.amount_animation = amount_animation
        self.now_animation = 0
        self.health = health
        self.image_file = image_file
        self.update_half = True
        self.speed = speed
        self.speed_for_move = self.speed
        self.dead_head = dead_head + 'zombie_dead_head_' + str(randint(0, 2)) + '.png'

    def update(self):
        global dead_zombie, zombie_end
        if self.update_half:
            self.rect.x -= self.speed
            self.image = transform.scale(image.load(self.image_file + str(self.now_animation) + '.png'),
                                         (self.rect.width, self.rect.height))
            self.now_animation += 1
            if self.now_animation == self.amount_animation:
                self.now_animation = 0
            self.update_half = not self.update_half
        else:
            self.update_half = not self.update_half
        if self.health <= 0:
            #sound_head_cut()
            zombies_dead_head = Zombie_Dead(self.dead_head, self.rect.x + self.rect.width * 0.1, self.rect.y + 5,
                                            55, 55, self.rect.bottom)
            zombie_dead_sprite.add(zombies_dead_head)
            dead_zombie += 1
            self.kill()
        if self.rect.x <= -75:
            zombie_end = True

class Zombie_FIRE(GameSprite):
    def __init__(self, picture, x, y, width, height):
        super().__init__(picture, x, y, width, height)
        self.time_die = timing.time()


    def zombie_fire_kill(self):
        global dead_zombie
        if timing.time() - self.time_die >= 3:
            dead_zombie += 1
            self.kill()

class Zombie_Dead(GameSprite):
    def __init__(self, picture, x, y, width, height, y_down):
        super().__init__(picture, x, y, width, height)
        self.time_die = timing.time()
        self.y_down = y_down
        self.sound_down = True


    def zombie_head_down(self):
        if self.rect.bottom < self.y_down:
            self.rect.y += 5
        elif timing.time() - self.time_die >= 4:
            self.kill()
        if self.rect.bottom > self.y_down - 10 and self.sound_down:
            self.sound_down = False
            sound_head_down()





class Plants(GameSprite):
    def __init__(self, picture, x, y, width, height, time_reset, amount_animation, health, image_file):
        super().__init__(picture, x, y, width, height)
        self.time_plants = timing.time()
        self.time_make = timing.time()
        self.cooldown = time_reset
        self.amount_animation = amount_animation
        self.now_animation = 0
        self.health = health
        self.health_full = health
        self.image_file = image_file
        self.update_True = True

    def update(self):
        if self.update_True:
            self.image = transform.scale(image.load(self.image_file + str(self.now_animation) + '.png'),
                                         (self.rect.width, self.rect.height))
            self.now_animation += 1
            if self.now_animation == self.amount_animation:
                self.now_animation = 0
            if self.health <= 0:
                for cell in cell_sprite:
                    if cell.rect.x == self.rect.x and cell.rect.y == self.rect.y:
                        cell.use = True
                        break
                zombie_eating_end()
                self.kill()


    def cheack_cooldown(self):
        self.time_make = timing.time()
        if self.time_make - self.time_plants >= self.cooldown:
            self.time_plants = self.time_make
            return True
        else:
            return False

class Lawn_mowers(GameSprite):
    def __init__(self, picture, x, y, width, height):
        super().__init__(picture, x, y, width, height)
        self.speed = 0
        self.touch = False
        self.first_touch = True

    def update(self):
        self.rect.x += self.speed
        self.prepared_speed = 10
        if self.rect.x >= window_width + 10:
            self.kill()
        if self.speed == self.prepared_speed and self.touch and self.first_touch:
            self.first_touch = False
            Lawn_Mower_Sound()
            #модуль для музыки газонокосилки!
            pass


class Peashooter(Plants):
    def Shoot(self):
        if self.cheack_cooldown() and len(zombie_sprite) != 0:
            bullet = Bullet('image/bullet/bullet_0.png', self.rect.right - 10, self.rect.y + 15, 32, 32, 8)
            bullets_sprite.add(bullet)
            sound_peashooter()


class Bullet(GameSprite):
    def __init__(self, picture, x, y, width, height, speed):
        super().__init__(picture, x, y, width, height)
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.x + 10 >= window_width:
            self.kill()


class Jalapeno(Plants):
    def Jalapeno_fire(self):
        if self.now_animation + 1 == self.amount_animation:
            self.Jalapeno_fire_created()
            self.kill()
            for cell in cell_sprite:
                if cell.rect.x == self.rect.x and cell.rect.y == self.rect.y:
                    cell.use = True
                    break

    def Jalapeno_fire_created(self):
        fire = Jalapeno_FIRE('image/plants/jalapeno/fire/fire0.png', 100, self.rect.y, 885, 100, 0, 25, 10,
                             'image/plants/jalapeno/fire/fire')
        FIRE_sprite.add(fire)
        #jalapeno_fire_sprite.add(fire)

class Cherry(Plants):
    def cherry_BOOM(self):
        if self.now_animation + 1 == self.amount_animation:
            self.cherry_BOOM_created()
            self.kill()
            for cell in cell_sprite:
                if cell.rect.x == self.rect.x and cell.rect.y == self.rect.y:
                    cell.use = True
                    break
    def cherry_BOOM_created(self):
        fire = Jalapeno_FIRE('image/plants/cherry/BOOM/boom0.png', self.rect.x - self.rect.width,
                             self.rect.y - self.rect.height, self.rect.width * 3, self.rect.height * 3, 0, 31, 10,
                             'image/plants/cherry/BOOM/boom')
        FIRE_sprite.add(fire)

class Jalapeno_FIRE(Plants):
    pass

class Wallnut(Plants):
    def replacement_image_health(self):
        if self.health <= 0.25 * self.health_full:
            self.update_True = False
            self.image = transform.scale(image.load('image/plants/wall-nut/Wallnut_25%.png'),
                                         (self.rect.width, self.rect.height))
        elif self.health <= 0.5 * self.health_full:
            self.update_True = False
            self.image = transform.scale(image.load('image/plants/wall-nut/Wallnut_50%.png'),
                                         (self.rect.width, self.rect.height))
        if self.health <= 0:
            for cell in cell_sprite:
                if cell.rect.x == self.rect.x and cell.rect.y == self.rect.y:
                    cell.use = True
                    break
            self.kill()


class Sunflower(Plants):
    def created_sun(self):
        if self.cheack_cooldown():
            if len(sun_sprite) < 2:
                sound_sunflower()
                y_sunflower = self.rect.y + randint(-50, 50)
                sun = suns('image/suns/sun_0.png', self.rect.x + randint(-50, 50), y_sunflower, 90, 90,
                           y_sunflower + randint(10, 50))
                sun_sprite.add(sun)
                self.cooldown = randint(19, 25)
            else:
                self.time_plants = self.time_make


click_on_cell = False
cancell_plants = GameSprite('image/cards/cancell_pay.png', 570, 8, 65, 88)
card = cards_sprite_class('image/cards/image_sunflower_card.png', 95, 8, 65, 90, 50, 10, 'sunflower')
card_2 = cards_sprite_class('image/cards/image_peashooter_card.png', 165, 8, 65, 90, 100, 12, 'peashooter')
card_3 = cards_sprite_class('image/cards/image_wallnut_card.png', 235, 8, 65, 90, 50, 10, 'wallnut')
card_4 = cards_sprite_class('image/cards/image_jalapeno_card.png', 305, 8, 65, 90, 125, 25, 'jalapeno')
card_5 = cards_sprite_class('image/cards/image_cherry_card.png', 375, 8, 65, 90, 150, 25, 'cherry')
shovel_cards = GameSprite('image/cards/image_shovel_card.png', 645, 0, 80, 80)
cards_sprite = sprite.Group()
cards_sprite.add(card)
cards_sprite.add(card_2)
cards_sprite.add(card_3)
cards_sprite.add(card_4)
cards_sprite.add(card_5)
cell_sprite = sprite.Group()
maker_cells()
suns_image_list = ['image/suns/sun_0.png', 'image/suns/sun_3.png', 'image/suns/sun_6.png', 'image/suns/sun_9.png',
                   'image/suns/sun_12.png']
lawn_mower_sprite = sprite.Group()
maker_lawn_mower()
sun_sprite = sprite.Group()
money_sun = 50 # МАНЕТЫ ЧТО БЫ ТЫ НЕ ЗАБЫЛ ИХ УБРАТЬ ДО 50
money_label = GameSprite('image/Black.jpg', 15, 76, 50, 30)
sun_end = GameSprite('image/black.jpg', -10, -10, 110, 120)
suns_end = sprite.Group()
suns_end.add(sun_end)
money_label.set_text(str(money_sun), 40, (0, 0, 0))
mouse_type = False
sunflower_sprite = sprite.Group()
peashooter_sprite = sprite.Group()
jalapeno_sprite = sprite.Group()
cherry_sprite = sprite.Group()
plants_sprite = sprite.Group()
FIRE_sprite = sprite.Group()
bullets_sprite = sprite.Group()
zombie_sprite = sprite.Group()
wallnut_sprite = sprite.Group()
time_first_zombie = 10
time_zombie_start = timing.time()
# time_zombie_end = timing.time()
spawn_zombie = False
first_zombie_was = True
time_zombie_respawn = 20

zombie_fire_sprite = sprite.Group()
zombie_dead_sprite = sprite.Group()

# clock = time.Clock()
def shovel_blit(shovel_enable):
    # global x_mouse, y_mouse
    x_mouse, y_mouse = mouse.get_pos()
    if shovel_enable:
        window.blit(transform.scale(image.load('image/cards/image_shovel.png'), (80, 80)), (x_mouse - 20, y_mouse - 60))


while flag_game:
    gameplay()
    time.delay(30)
    for e in event.get():
        if e.type == QUIT:
            flag_game = False
        elif e.type == MOUSEBUTTONDOWN and e.button == 1:
            x_mouse, y_mouse = e.pos
            mouse_type = True
            # print(x_mouse, y_mouse)

    if mouse_type:
        for i in sun_sprite:
            i.collede_sun_mouse(x_mouse, y_mouse)
        for i in cards_sprite:
            i.collede_cards_mouse(x_mouse, y_mouse)
        mouse_type = False
        if click_on_cell:
            for i in cell_sprite:
                foo_click_cells = i.collede_cells_mouse(x_mouse, y_mouse)
                if foo_click_cells != None:
                    plants_give()
                    x_plant, y_plant = foo_click_cells
                    if type_plant == 'sunflower':
                        sunflower = Sunflower('image/plants/sunflower/sunflower_0.png', x_plant, y_plant, 100, 100,
                                              randint(3, 5), 54, 100, 'image/plants/sunflower/sunflower_')  # 54
                        plants_sprite.add(sunflower)
                        sunflower_sprite.add(sunflower)
                    elif type_plant == 'peashooter':
                        peashooter = Peashooter('image/plants/peashooter_normal/peashooter_0.png', x_plant, y_plant,
                                                100, 100, 3, 96, 100, 'image/plants/peashooter_normal/peashooter_')  # 96
                        plants_sprite.add(peashooter)
                        peashooter_sprite.add(peashooter)
                    elif type_plant == 'wallnut':
                        wallnut = Wallnut('image/plants/wall-nut/Wallnut_0.png', x_plant, y_plant, 100, 100, 0, 64, 1000,
                                          'image/plants/wall-nut/Wallnut_')
                        plants_sprite.add(wallnut)
                        wallnut_sprite.add(wallnut)
                    elif type_plant == 'jalapeno':
                        jalapeno = Jalapeno('image/plants/jalapeno/jalapeno_0.png', x_plant, y_plant, 100, 100, 0, 10, 1000,
                                         'image/plants/jalapeno/jalapeno_')
                        plants_sprite.add(jalapeno)
                        jalapeno_sprite.add(jalapeno)
                        jalapeno_FIRE()
                    elif type_plant == 'cherry':
                        cherry = Cherry('image/plants/cherry/cherry_0.png', x_plant, y_plant, 100, 100, 0, 17, 1000,
                                         'image/plants/cherry/cherry_')
                        plants_sprite.add(cherry)
                        cherry_sprite.add(cherry)
                        cherry_BOOM()
                    type_plant = ''
            if cancell_plants.collede_mouse(x_mouse, y_mouse):
                money_sun += price_for_cancell
                cancell_pay()
                click_on_cell = False
            if shovel_push:
                shovel_push = False
                shovel_cancel()
                shovel_cards.image = transform.scale(image.load('image/cards/image_shovel_card.png'),
                                                     (shovel_cards.rect.width, shovel_cards.rect.height))

        elif shovel_cards.collede_mouse(x_mouse, y_mouse) and not shovel_push:
            shovel_enable()
            shovel_cards.image = transform.scale(image.load('image/cards/image_shovel_card_enable.png'),
                                                 (shovel_cards.rect.width, shovel_cards.rect.height))
            shovel_push = True
            shovel_cancel_push = False

        if shovel_push:
            if shovel_cards.collede_mouse(x_mouse, y_mouse) and shovel_cancel_push:
                shovel_cancel_push = False
                shovel_cards.image = transform.scale(image.load('image/cards/image_shovel_card.png'),
                                                     (shovel_cards.rect.width, shovel_cards.rect.height))
                shovel_cancel()
                shovel_push = False
            else:
                shovel_cancel_push = True
            for i in plants_sprite:
                if i.collede_mouse(x_mouse, y_mouse):
                    x_cell_plant = i.rect.x
                    y_cell_plant = i.rect.y
                    # print(i.rect.x, i.rect.y)
                    i.kill()
                    for i in cell_sprite:
                        if i.rect.x == x_cell_plant and i.rect.y == y_cell_plant:
                            i.use = True
                            break
                    shovel_work()
                    shovel_cards.image = transform.scale(image.load('image/cards/image_shovel_card.png'),
                                                         (shovel_cards.rect.width, shovel_cards.rect.height))
                    shovel_push = False
                    break

    for i in sunflower_sprite:
        i.created_sun()

    for i in peashooter_sprite:
        i.Shoot()

    for i in sun_sprite:
        i.collected()

    for i in jalapeno_sprite:
        i.Jalapeno_fire()

    for i in cherry_sprite:
        i.cherry_BOOM()

    for i in wallnut_sprite:
        i.replacement_image_health()

    for i in FIRE_sprite:
        if i.now_animation + 1 == i.amount_animation:
            i.kill()

    for i in zombie_fire_sprite:
        i.zombie_fire_kill()

    for i in zombie_dead_sprite:
        i.zombie_head_down()

    if timing.time() - time_zombie_start >= time_first_zombie and first_zombie_was:
        zombie = Zombie('image/zombies/zombie_normal/0.png', window_width + 10,
                        zombies_y_list[randint(0, len(zombies_y_list) - 1)] - 20, 90, 130, 15, 100,
                        'image/zombies/zombie_normal/', 1, 'image/zombies/zombie_normal/')
        zombie_sprite.add(zombie)
        first_zombie_was = False
        spawn_zombie = True
        time_zombie_start = timing.time()
        sound_zombie_begin()

    if spawn_zombie:
        # print(time_zombie_respawn)
        if timing.time() - time_zombie_start >= time_zombie_respawn and len(zombie_sprite) < 6:
            if time_zombie_respawn > 3:
                time_zombie_respawn -= 1
            else:
                time_zombie_respawn = 17
            random_zombie = randint(0, 7)
            if random_zombie == 0 or random_zombie == 1:
                zombie = Zombie('image/zombies/zombie_normal/0.png', window_width + 10,
                                zombies_y_list[randint(0, len(zombies_y_list) - 1)] - 20, 90, 130, 15, 100,
                                'image/zombies/zombie_normal/', 1, 'image/zombies/zombie_normal/')
            elif random_zombie == 2 or random_zombie == 3:
                zombie = Zombie('image/zombies/zombie_dancing/0.png', window_width + 10,
                                zombies_y_list[randint(0, len(zombies_y_list) - 1)] - 20, 90, 130, 33, 100,
                                'image/zombies/zombie_dancing/', 1, 'image/zombies/zombie_dancing/')
            elif random_zombie == 4:
                zombie = Zombie('image/zombies/zombie_bucket/zombie_bucket_0.png', window_width + 10,
                                zombies_y_list[randint(0, len(zombies_y_list) - 1)] - 20, 90, 130, 15, 200,
                                'image/zombies/zombie_bucket/zombie_bucket_', 1, 'image/zombies/zombie_bucket/')
            elif random_zombie == 5:
                zombie = Zombie('image/zombies/zombie_football/zombie_football_0.png', window_width + 10,
                                zombies_y_list[randint(0, len(zombies_y_list) - 1)] - 20, 120, 130, 1, 200,
                                'image/zombies/zombie_football/zombie_football_', 2, 'image/zombies/zombie_football/')
            elif random_zombie == 7 or random_zombie == 6:
                zombie = Zombie('image/zombies/zombie_cap/0.png', window_width + 10,
                                zombies_y_list[randint(0, len(zombies_y_list) - 1)] - 20, 100, 130, 15, 100,
                                'image/zombies/zombie_cap/', 1, 'image/zombies/zombie_cap/')
            zombie_sprite.add(zombie)
            time_zombie_start = timing.time()

    if len(zombie_sprite) != 0 and randint(0, 1000) == 0:
        sound_zombie()

    if sprite.groupcollide(zombie_sprite, bullets_sprite, False, False): #косание зомбей с пулями (горохом)
        sound_bullet()
        for zombie in sprite.groupcollide(zombie_sprite, bullets_sprite, False, True):
            zombie.health -= 10

    if dead_zombie >= 10:
        music_end_good()
        while True:
            final_image = image.load('image/ZombiesLose.jpg')
            window.blit(transform.scale(final_image, (window_width, window_height)), (0, 0))
            event_exit()
            display.update()

    if zombie_end:
        music_end_bad()
        while True:
            final_image = image.load('image/ZombiesWon.jpg')
            window.blit(transform.scale(final_image, (window_width, window_height)), (0, 0))
            event_exit()
            display.update()

    for zombie in zombie_sprite: #что бы зомби когда съедал растения шел опять с той же скоростью как и с начала
        zombie.speed = zombie.speed_for_move

    for zombie in sprite.groupcollide(zombie_sprite, FIRE_sprite, True, False):
        fire_zombie = Zombie_FIRE('image/zombies/zombie_fire/0.png', zombie.rect.x, zombie.rect.y, zombie.rect.width, zombie.rect.height)
        zombie_fire_sprite.add(fire_zombie)


    if sprite.groupcollide(lawn_mower_sprite, zombie_sprite, False, False):
        for lawn_mowers in sprite.groupcollide(lawn_mower_sprite, zombie_sprite, False, False):
            lawn_mowers.speed = lawn_mowers.prepared_speed
            lawn_mowers.touch = True
        for zombie in sprite.groupcollide(zombie_sprite, lawn_mower_sprite, False, False):
            zombie.health = 0

    if sprite.groupcollide(plants_sprite, zombie_sprite, False, False):
        if playing == 0:
            zombie_eating()
            playing += 1
        else:
            playing += 1
        if playing >= 25:
            playing = 0
        for plant in sprite.groupcollide(plants_sprite, zombie_sprite, False, False):
            #zombie.speed = 0
            plant.health -= 1
        for zombie in sprite.groupcollide(zombie_sprite, plants_sprite, False, False):
            #zombie.speed = 0
            zombie.speed = 0

    display.update()