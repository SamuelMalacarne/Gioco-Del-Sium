import pygame
import random
import sys

pygame.init()

HEIGHT = 400
WIDTH = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont('arial', 25)
small_font = pygame.font.SysFont('arial', 20)

sounds = ['\sium1', '\sium2', '\sium3', '\sium4', '\sium5', '\sium6']
scoring_sounds = list()

for sound in sounds:
    scoring_sounds.append(pygame.mixer.Sound('.\data\sounds' + sound + '.mp3'))

icon_image = pygame.image.load('.\data\sprites\piazz.png')
pygame.display.set_caption('Gioco Del Sium')
pygame.display.set_icon(icon_image)
screen.fill('light blue')

score = 0
playing = False
start = True
obstacles = list()
obstacle_height = 250
space_between_top_and_bot_obstacles = 160
space_between_obstacles = 200

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.velocity = -2
        self.surface = pygame.image.load('.\data\sprites\stampella.png').convert_alpha()
        self.surface = pygame.transform.scale(self.surface, (50, obstacle_height))
        self.rect = self.surface.get_rect(midtop = self.pos)
        self.mask = pygame.mask.from_surface(self.surface)

    def update(self):
        self.pos[0] += self.velocity
        self.rect = self.surface.get_rect(topright = self.pos)
        return self.pos

class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.speed = 2
        self.x = 100
        self.y = 100
        self.acceleration = 0.2
        self.surface = pygame.image.load('.\data\sprites\piazz.png').convert_alpha()
        self.surface = pygame.transform.scale(self.surface, (40, 40))
        self.rect = self.surface.get_rect(center = (self.x, self.y))
        self.mask = pygame.mask.from_surface(self.surface)    

    def reset(self):
        self.speed = 2
        self.x = 100
        self.y = 100
        self.acceleration = 0.5
        self.jump_height = 9
        self.rect = self.surface.get_rect(center = (self.x, self.y))
    
    def jump(self):
        self.speed = -self.jump_height

    def update_pos(self):
        self.speed += self.acceleration
        self.y += self.speed

        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            prepare_after_dead()

        self.rect = self.surface.get_rect(center = (self.x, self.y))

    def update_img(self):
        self.surface = pygame.image.load('.\data\sprites\sium_piazz.png' if pygame.mixer.get_busy() else '.\data\sprites\piazz.png').convert_alpha()
        self.surface = pygame.transform.scale(self.surface, (40, 40))

def initialize_obstacles():
    for i in range(0, 4):
        y_positions = choose_y_pos()
        x_pos = (i*space_between_obstacles)+500
        obstacles.append([Obstacle([x_pos, y_positions[0]]), Obstacle([x_pos, y_positions[1]])])
        obstacles_sprite.add(obstacles[i][0])
        obstacles_sprite.add(obstacles[i][1])

def update_obstacle_pair(obs_pair):
    obs_pair[0].pos[0] = WIDTH + space_between_obstacles
    obs_pair[1].pos[0] = WIDTH + space_between_obstacles

    y_positions = choose_y_pos()
    obs_pair[0].pos[1] = y_positions[0]
    obs_pair[1].pos[1] = y_positions[1]

def choose_y_pos():
    top_obs_y = -random.randrange(5, obstacle_height)
    bot_obs_y = top_obs_y + obstacle_height + space_between_top_and_bot_obstacles

    return [top_obs_y, bot_obs_y]

def prepare_after_dead():
    global playing, start, obstacles
    playing = False
    start = False
    obstacles = list()
    pygame.mixer.stop()
    screen.fill('light blue')

player = Player()

score_text_surface = font.render(f'sium: {score}', True, 'blue')

loosing_img = pygame.image.load('.\data\sprites\sad_piazz.png').convert_alpha()
start_img = pygame.image.load('.\data\sprites\start_piazz.png').convert_alpha()

loosing_text_l1 = font.render('Hai perso :(', True, 'blue')
l_t_l1_rect = loosing_text_l1.get_rect(center = ((WIDTH/4)*3, (HEIGHT/2)-20))
loosing_text_l2 = small_font.render('Premi spazio per ricominciare', True, 'blue')
l_t_l2_rect = loosing_text_l2.get_rect(center = ((WIDTH/4)*3, (HEIGHT/2)+20))
starting_text = font.render('Premi spazio per iniziare', True, 'blue')
s_t_rect = starting_text.get_rect(center = ((WIDTH/4)*3, HEIGHT/2))


# player_for_collision = pygame.sprite.GroupSingle(player)

sprites = pygame.sprite.Group()
obstacles_sprite = pygame.sprite.Group()

sprites.add(player)

while True:

    if playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
                    player.update_pos()
        
        screen.fill('light blue')

        screen.blit(score_text_surface, (0, 0))

        for obstacle_pair in obstacles:
            screen.blit(obstacle_pair[0].surface, obstacle_pair[0].rect)
            screen.blit(obstacle_pair[1].surface, obstacle_pair[1].rect)

        player.update_img()

        screen.blit(player.surface, player.rect)

        player.update_pos()

        for obstacle_pair in obstacles:

            if pygame.sprite.collide_mask(player, obstacle_pair[0]) != None or pygame.sprite.collide_mask(player, obstacle_pair[1]) != None:
                prepare_after_dead()

            # x positions are the same
            x_pos = obstacle_pair[0].update()[0]
            obstacle_pair[1].update()

            if x_pos <= 0:
                update_obstacle_pair(obstacle_pair)
            elif x_pos == player.x:
                random.choice(scoring_sounds).play()
                score += 1
                score_text_surface = font.render(f'sium: {score}', True, 'blue')

        pygame.display.update()
        clock.tick(60)

    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.reset()
                    score = 0
                    initialize_obstacles()
                    score_text_surface = font.render(f'sium: {score}', True, 'blue')

                    playing = True

        if start:
            screen.blit(start_img, (0, 0))
            screen.blit(starting_text, s_t_rect)
        else:
            screen.blit(loosing_img, (0, 0))
            screen.blit(loosing_text_l1, l_t_l1_rect)
            screen.blit(loosing_text_l2, l_t_l2_rect)

        pygame.display.update()
        clock.tick(60)