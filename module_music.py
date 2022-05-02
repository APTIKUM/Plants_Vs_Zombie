from random import randint
from pygame import *
mixer.pre_init(44100, -16, 1, 512)

sun_sound_list = ['sun_1.ogg', 'sun_2.ogg', 'sun_3.ogg', 'sun_4.ogg', 'sun_5.ogg', 'sun_6.ogg', 'sun_7.ogg'] # список что бы не повторялись звуки при сборе солнышек

# фоновая музня
def backmusic():
    mixer.music.load('sounds/background/plants_vs_zombies_02 - Crazy Dave (Intro Theme).mp3')
    mixer.music.play(-1)
    mixer.music.set_volume(0.06)


def music_end_good():
    mixer.music.stop()
    mixer.music.load('sounds/background/PVZ_END_GOOD.mp3')
    mixer.music.play(-1)
    mixer.music.set_volume(0.06)

def music_end_bad():
    mixer.music.stop()
    mixer.music.load('sounds/background/Plants_vs_Zombies_END_BAD.mp3')
    mixer.music.play(0)
    mixer.music.set_volume(0.06)

# когда солнышко собираем
def sound_sun():
    sound = mixer.Sound('sounds/sun/' + sun_sound_list[randint(0, len(sun_sound_list) - 1)])
    mixer.Sound.set_volume(sound, 0.4)
    sound.play()

# при нажатие на карточки (покупка растения)
def plants_pay(price):
    if price:
        sound = mixer.Sound('sounds/plants/plants_take.ogg')
        mixer.Sound.set_volume(sound, 0.4)
        sound.play()
    else:
        sound = mixer.Sound('sounds/plants/sound_have_no_money.ogg')
        mixer.Sound.set_volume(sound, 0.4)
        sound.play()

# сажаем растения
def plants_give():
    sound = mixer.Sound('sounds/plants/plants_give.ogg')
    mixer.Sound.set_volume(sound, 0.4)
    sound.play()

# когда схватки у подсолнуха и он рожает солнце
def sound_sunflower():
    sound = mixer.Sound('sounds/plants/sunflower/sunflower_sound.ogg')
    mixer.Sound.set_volume(sound, 0.4)
    sound.play()

def cancell_pay():
    sound = mixer.Sound('sounds/plants/sound_have_no_money.ogg')
    mixer.Sound.set_volume(sound, 0.4)
    sound.play()

def sound_peashooter():
    sound = mixer.Sound('sounds/plants/peashooter/peashooter_sound.ogg')
    mixer.Sound.set_volume(sound, 0.4)
    sound.play()

def sound_zombie_begin():
    sound = mixer.Sound('sounds/zombie/zombie_begin.ogg')
    mixer.Sound.set_volume(sound, 0.4)
    sound.play()

def sound_zombie():
    sound = mixer.Sound('sounds/zombie/zombie_sound.ogg')
    mixer.Sound.set_volume(sound, 0.4)
    sound.play()

def sound_bullet():
    sound = mixer.Sound('sounds/plants/bullet/bullet.ogg')
    mixer.Sound.set_volume(sound, 0.4)
    sound.play()

def shovel_enable():
    sound = mixer.Sound('sounds/shovel/shovel_enable.ogg')
    mixer.Sound.set_volume(sound, 0.4)
    sound.play()

def shovel_cancel():
    sound = mixer.Sound('sounds/shovel/shovel_cancel.ogg')
    mixer.Sound.set_volume(sound, 0.4)
    sound.play()

def shovel_work():
    sound = mixer.Sound('sounds/shovel/shovel_work.ogg')
    mixer.Sound.set_volume(sound, 0.4)
    sound.play()


def zombie_eating():
    sound = mixer.Sound('sounds/zombie/zombie_eating.ogg')
    mixer.Sound.set_volume(sound, 0.4)
    sound.play()

def zombie_eating_end():
    sound = mixer.Sound('sounds/zombie/zombie_eating_end.ogg')
    mixer.Sound.set_volume(sound, 0.4)
    sound.play()

def jalapeno_FIRE():
    sound = mixer.Sound('sounds/plants/jalapeno/jalapeno_FIRE.ogg')
    mixer.Sound.set_volume(sound, 0.4)
    sound.play()

def cherry_BOOM():
    sound = mixer.Sound('sounds/plants/cherry/cherry_BOOM.ogg')
    mixer.Sound.set_volume(sound, 0.4)
    sound.play()

def Lawn_Mower_Sound():
    sound = mixer.Sound('sounds/lawn_mower/lawn_mower.ogg')
    mixer.Sound.set_volume(sound, 0.4)
    sound.play()

def sound_head_cut():
    sound = mixer.Sound('sounds/zombie/sound_cut_head.ogg')
    mixer.Sound.set_volume(sound, 0.4)
    sound.play()

def sound_head_down():
    sound = mixer.Sound('sounds/zombie/sound_head_down.ogg')
    mixer.Sound.set_volume(sound, 0.6)
    sound.play()