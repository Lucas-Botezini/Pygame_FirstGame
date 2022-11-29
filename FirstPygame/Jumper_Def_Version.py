import pygame
from sys import exit # Import the Sys so you can close the game
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        player_walk1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk1, player_walk2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.wav')
        self.jump_sound.set_volume(0.4)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def player_anima(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.player_anima()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == "fly":
            fly_frame1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()  # Enemy image - Use "convert_alpha()" in the Enemy
            fly_frame2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_frame1, fly_frame2]
            y_pos = 200
        else:
            snail_frame1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()  # Enemy image - Use "convert_alpha()" in the Enemy
            snail_frame2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame1, snail_frame2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

    def obstacle_anima(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.obstacle_anima()

        if current_time < 10:
            self.rect.x -= 4
        elif current_time <= 25:
            self.rect.x -=5
        elif current_time > 25:
            self.rect.x -= 6

        elif current_time > 60:
            self.rect.x -= 8

        elif current_time > 90:
            self.rect.x -= 10
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    global current_time

    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f"Tempo: {current_time}s", False, "Black")  # Score of the game
    score_rect = score_surf.get_rect(midright=(750,30))
    screen.blit(score_surf,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:

            if current_time < 10:
                obstacle_rect.x -= 4

            elif current_time <= 25:
                obstacle_rect.x -= 5

            elif current_time > 25:
                obstacle_rect.x -= 6

            elif current_time > 60:
                obstacle_rect.x -= 8

            elif current_time > 90:
                obstacle_rect.x -= 10

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -50]
        return obstacle_list
    else:
        return[]

def collision(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False

    return True
def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group, False): # IF the last condition is TRUE, the 2°arg will be destroyed
        obstacle_group.empty()
        return False
    else:
        return True
def player_animation():
    global player_surface, player_index

    if player_rect.bottom < 300:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0

        player_surface = player_walk[int(player_index)]

pygame.init() # Start the pygame

# Opening the game screen and Icons
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Jumper')
gameIcon = pygame.image.load('graphics/icon.png')
pygame.display.set_icon(gameIcon)
score = 0

# Bk Music
back_ground_music = pygame.mixer.Sound('audio/music.wav')
back_ground_music.set_volume(0.2)
back_ground_music.play(loops = -1)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

# Font and Fps counter
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 30)


game_active = False     # Here we are setting the game activation to false

start_time = 0      # Here we count the time and use it in the display_score()

            # All images in the graphics need to contain a ".convert()" so pygame can work better

# Graphics Images           - The order displayed here, is the order they program will read the images
sky_surface = pygame.image.load('Images/Sky.png').convert()     # Add a Image
ground_surface = pygame.image.load('graphics/ground.png').convert() # Convert() is used so pygame can run the game better
text1 = "The Jumper"
text_surface = test_font.render( text1, False, "Red") # Write the text, say if you want him Anti-Aliase, set the color


obstacle_rect_list = []

# Player
player_walk1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()   # Import of the imgs to the player animation
player_walk2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk1, player_walk2]      # The list between the two walks

player_index = 0        # This is the index that will be used to make the list work
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()     # The jump of the player

player_surface = player_walk[player_index]     # This will make the animation between walk1 and walk2

player_rect = player_surface.get_rect(midbottom=(80, 300))
player_gravity = 0

# Intro Screen
player_surface_intro = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_surface_intro = pygame.transform.scale2x(player_surface_intro)
player_intro_rect = player_surface_intro.get_rect(center=(400, 200))

text_rect = text_surface.get_rect(center = (400,30))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1400)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 600)

fly_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(fly_animation_timer, 300)

while True:     # Loop to run the game, and to update it.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # Event to close the game
            pygame.quit()
            exit()

        if game_active:

# Events
            if event.type == pygame.MOUSEBUTTONDOWN:    # This gives the mouse position, but only if you move it "MOUSEMOTION"
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                    player_gravity = -10

            if event.type == obstacle_timer and game_active:

                obstacle_group.add(Obstacle(choice(['fly','fly','snail','snail','snail'])))

                # if randint(0,2):

                #     obstacle_rect_list.append(snail_surf.get_rect(midbottom=(randint(900,1100),300)))
                # else:
                #     obstacle_rect_list.append(fly_surf.get_rect(midbottom=(randint(900, 1100), 200)))


# Event Key Input

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and player_rect.bottom >= 300:
                    player_gravity = -12
        else:


            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                game_active = True
                # snail_rect.left = 800
                start_time = int(pygame.time.get_ticks() / 1000)


# BE CAREFUL in the order that is written the code, because this is how WILL APPEAR
    if game_active:
        screen.blit(sky_surface,(0,0))      # Add things to the surface
        screen.blit(ground_surface,(0,300))
        # pygame.draw.rect(screen,(16, 235, 213), score_rect,0,10) # Draw Rect, search to view the needs to draw it
        # screen.blit(text_surface,text_rect)
        # screen.blit(score_surf,score_rect)
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()


        game_active = collision_sprite()

    else:
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 300)
        player_gravity = 0
        screen.fill((94, 129 , 162))


        name = "The Jumper Game"
        name_surface = test_font.render(name, False, "Black")
        name_rect = name_surface.get_rect(topleft = (40, 30))
        screen.blit(name_surface,name_rect)

        text1 = "Para comecar o jogo aperte UP"
        text_surface = test_font.render(text1, False, "Black")
        text_rect = text_surface.get_rect(topright=(760, 30))

        score_message = test_font.render(f"Seu tempo foi {score}s", False, "Black")
        score_rect = score_message.get_rect(topright = (760,30))

        screen.blit(player_surface_intro, player_intro_rect)

        if score == 0:
            screen.blit(text_surface, text_rect)
        else:
            screen.blit(score_message,score_rect)





    pygame.display.update()
    clock.tick(60)      # Say how many times the image is updated in a second, try putting it to 1 or 600 to test. Use the clock var called back then
