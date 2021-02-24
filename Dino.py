import pygame
import random
import time

from storage import FileSave

dir_imgs = 'asserts/imgs/'
dir_audio = 'asserts/audio/'
dir_fonts = 'asserts/fonts/'

pygame.init()

save_score = FileSave.get()
display_width = 800
display_height = 600

display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('ORA ORA ORA')

pygame.mixer.music.load(dir_audio + 'Heroes.mp3')
pygame.mixer.music.set_volume(0.3)

hp_up_sound = pygame.mixer.Sound(dir_audio + 'hp.wav')
dmg_sound = pygame.mixer.Sound(dir_audio + 'dmg.wav')
smert_sound = pygame.mixer.Sound(dir_audio + 'smert.wav')
jump_sound = pygame.mixer.Sound(dir_audio + 'jump.wav')
fall_sound = pygame.mixer.Sound(dir_audio + 'fall.wav')
exit_sound = pygame.mixer.Sound(dir_audio + 'exit.wav')
collision_sound = pygame.mixer.Sound(dir_audio + 'collision.wav')
pause_sound = pygame.mixer.Sound(dir_audio + 'Za_Warudo.wav')
unpause_sound = pygame.mixer.Sound(dir_audio + 'unpause.wav')

icon = pygame.image.load(dir_imgs + 'iconOOP.png')
pygame.display.set_icon(icon)

cactus_img = [pygame.image.load(dir_imgs + 'cactus1.png'), pygame.image.load(dir_imgs + 'cactus2.png'),
              pygame.image.load(dir_imgs + 'cactus3.png')]
cactus_options = [20, 430, 30, 450, 25, 420]

stone_img = [pygame.image.load(dir_imgs + 'stone1.png'), pygame.image.load(dir_imgs + 'stone2.png'),
             pygame.image.load(dir_imgs + 'stone3.png'),
             pygame.image.load(dir_imgs + 'stone4.png'), pygame.image.load(dir_imgs + 'stone5.png'),
             pygame.image.load(dir_imgs + 'stone6.png')]
cloud_img = [pygame.image.load(dir_imgs + 'cloud1.png'), pygame.image.load(dir_imgs + 'cloud2.png')]

pers_img = [pygame.image.load(dir_imgs + 'pers1.png'), pygame.image.load(dir_imgs + 'pers2.png'),
            pygame.image.load(dir_imgs + 'pers3.png')]

hp_img = pygame.image.load(dir_imgs + 'milk.png')
hp_img = pygame.transform.scale(hp_img, (30, 30))

img_counter = 0
hp = 1
max_hp = 3


class Object:
    def __init__(self, x, y, width, image, speed):
        self.x = x
        self.y = y
        self.width = width
        self.image = image
        self.speed = speed

    def move(self):
        if self.x >= -self.width:
            display.blit(self.image, (self.x, self.y))
            self.x -= self.speed
            return True
        else:
            return False

    def return_self(self, radius, y, width, image):
        self.x = radius
        self.y = y
        self.width = width
        self.image = image
        display.blit(self.image, (self.x, self.y))


usr_width = 40
usr_heigth = 100
usr_x = display_width // 2
usr_y = display_height - usr_heigth - 100

cactus_width = 20
cactus_height = 70
cactus_x = display_width - 100
cactus_y = display_height - cactus_height - 100

clock = pygame.time.Clock()

make_jump = False
jump_counter = 30

scores = 0
max_above = 0


def run_game():
    global make_jump

    pygame.mixer.music.play(-1)

    game = True
    cactus_arr = []
    create_cactus_arr(cactus_arr)
    land = pygame.image.load(dir_imgs + 'fon.png')

    stone, cloud = open_random_objects()
    heart = Object(display_width, 280, 30, hp_img, 4)

    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            make_jump = True
        if keys[pygame.K_ESCAPE]:
            pygame.mixer.music.pause()
            pygame.mixer.Sound.play(pause_sound)
            pause()

        if make_jump:
            jump()

        count_scores(cactus_arr)

        display.blit(land, (0, 0))
        print_text('Pause: Esc', 10, 10)
        print_text('Scores: ' + str(scores) + '/' + str(save_score), 600, 10)

        draw_array(cactus_arr)
        move_object(stone, cloud)

        draw_pers()

        heart.move()
        hearts_plus(heart)

        if check_collision(cactus_arr):
            pygame.mixer.music.stop()
            # pygame.mixer.Sound.play()
            # if not check_hp():
            game = False

        show_hp()

        pygame.display.update()
        clock.tick(70)
    return game_over()


def jump():
    global usr_y, jump_counter, make_jump
    if jump_counter >= -30:
        if jump_counter == 30:
            pygame.mixer.Sound.play(jump_sound)
        if jump_counter == -10:
            pygame.mixer.Sound.play(fall_sound)

        usr_y -= jump_counter / 2.5
        jump_counter -= 1
    else:
        jump_counter = 30
        make_jump = False


def create_cactus_arr(array):
    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 20, height, width, img, 4))

    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 300, height, width, img, 4))

    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 600, height, width, img, 4))


def find_radius(array):
    maximum = max(array[0].x, array[1].x, array[2].x)

    if maximum < display_width:
        radius = display_width
        if radius - maximum < 50:
            radius += 280
    else:
        radius = maximum
    choice = random.randrange(0, 5)
    if choice == 0:
        radius += random.randrange(10, 15)
    else:
        radius += random.randrange(250, 400)

    return radius


def draw_array(array):
    for cactus in array:
        check = cactus.move()
        if not check:
            object_return(array, cactus)
            '''radius = find_radius(array)

            choice = random.randrange(0, 3)
            img = cactus_img[choice]
            width = cactus_options[choice * 2]
            height = cactus_options[choice * 2 + 1]

            cactus.return_self(radius, height, width, img)'''


def object_return(objects, obj):
    radius = find_radius(objects)

    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = cactus_options[choice * 2]
    height = cactus_options[choice * 2 + 1]

    obj.return_self(radius, height, width, img)


def open_random_objects():
    choice = random.randrange(0, 6)
    img_of_stone = stone_img[choice]

    choice = random.randrange(0, 2)
    img_of_cloud = cloud_img[choice]

    stone = Object(display_width, display_height - 80, 10, img_of_stone, 4)
    cloud = Object(display_width, 80, 100, img_of_cloud, 2)

    return stone, cloud


def move_object(stone, cloud):
    check = stone.move()
    if not check:
        choice = random.randrange(0, 6)
        img_of_stone = stone_img[choice]
        stone.return_self(display_width, 500 + random.randrange(1, 90), stone.width, img_of_stone)

    check = cloud.move()
    if not check:
        choice = random.randrange(0, 2)
        img_of_cloud = cloud_img[choice]
        cloud.return_self(display_width, random.randrange(10, 200), cloud.width, img_of_cloud)


def draw_pers():
    global img_counter
    if img_counter == 30:
        img_counter = 0

    display.blit(pers_img[img_counter // 10], (usr_x, usr_y))
    img_counter += 1


def print_text(message, x, y, font_color=(0, 0, 0), font_type=dir_fonts + 'poi.ttf', font_size=30):
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)
    display.blit(text, (x, y))


def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text('Пауза.', 160, 200)
        keys = pygame.key.get_pressed()
        pygame.display.update()
        clock.tick(15)
        if keys[pygame.K_RETURN]:
            pygame.mixer.pause()
            pygame.display.update()
            pygame.mixer.Sound.play(unpause_sound)
            pygame.mixer.music.unpause()
            paused = False


def check_collision(barriers):
    for barrier in barriers:
        if usr_y + usr_heigth >= barrier.y:
            if barrier.x <= usr_x <= barrier.x + barrier.width:
                if check_hp():
                    object_return(barriers, barrier)
                    return False
                else:
                    return True
            elif barrier.x <= usr_x + usr_width <= barrier.x + barrier.width:
                if check_hp():
                    object_return(barriers, barrier)
                    return False
                else:
                    return True
    return False


def count_scores(barriers):
    global scores, max_above
    above_cactus = 0

    if -20 <= jump_counter < 25:
        for barrier in barriers:
            if usr_y + usr_heigth - 5 <= barrier.y:
                if barrier.x <= usr_x <= barrier.x + barrier.width:
                    above_cactus += 1
                elif barrier.x <= usr_x <= barrier.x + barrier.width:
                    above_cactus += 1

        max_above = max(max_above, above_cactus)
    else:
        if jump_counter == -30:
            scores += max_above
            max_above = 0


def game_over():
    FileSave.save(max(scores, save_score))
    stopped = True
    while stopped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text('Game over. Press Enter to play again, Esc to exit.', 40, 200)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            pygame.mixer.pause()
            return True
        if keys[pygame.K_ESCAPE]:
            return False

        pygame.display.update()
        clock.tick(15)


def show_hp():
    global hp
    show = 0
    x = 20
    while show != hp:
        display.blit(hp_img, (x, 50))
        x += 40
        show += 1


def check_hp():
    global hp
    hp -= 1
    if hp == 0:
        pygame.mixer.Sound.play(collision_sound)
        pygame.mixer.Sound.play(smert_sound)
        return False
    else:
        pygame.mixer.Sound.play(dmg_sound)
        return True


def hearts_plus(heart):
    global hp, usr_x, usr_y, usr_width, usr_heigth
    if usr_x <= heart.x <= usr_x + usr_width:
        if usr_y <= heart.y <= usr_y + usr_heigth:
            pygame.mixer.Sound.play(hp_up_sound)
            if hp < 5:
                hp += 1

            radius = display_width + random.randrange(500, 10000)
            heart.return_self(radius, heart.y, heart.width, heart.image)


while run_game():
    scores = 0
    make_jump = False
    jump_counter = 30
    usr_y = display_height - usr_heigth - 100
    hp = 1
pygame.mixer.pause()
pygame.mixer.Sound.play(exit_sound)
time.sleep(1.5)
pygame.quit()
quit()
