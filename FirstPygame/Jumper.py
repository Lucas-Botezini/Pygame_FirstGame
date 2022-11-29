import pygame
from sys import exit # Import the Sys so you can close the game
from random import randint

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
screen = pygame.display.set_mode((800, 400))  # First number is width and Second is height. This is the screen of the game
pygame.display.set_caption('Jumper')    # Set the title of the game
gameIcon = pygame.image.load('graphics/icon.png')  # Set the icon in a var
pygame.display.set_icon(gameIcon)   # Set the icon in the game
score = 0       # Score that is the timer

# Font and Fps counter
clock = pygame.time.Clock()     # Add a timer - Help to set the Frames Per Second (fps) - You have to put it in the "while True" loop to work
test_font = pygame.font.Font('font/Pixeltype.ttf', 30)   # Add a font (fonte, tamanho da fonte)


game_active = False     # Here we are setting the game activation to false

start_time = 0      # Here we count the time and use it in the display_score()

            # All images in the graphics need to contain a ".convert()" so pygame can work better

# Graphics Images           - The order displayed here, is the order they program will read the images
sky_surface = pygame.image.load('Images/Sky.png').convert()     # Add a Image
ground_surface = pygame.image.load('graphics/ground.png').convert() # Convert() is used so pygame can run the game better
text1 = "The Jumper"
text_surface = test_font.render( text1, False, "Red") # Write the text, say if you want him Anti-Aliase, set the color


# score_surf = test_font.render('Score: ', False, "Black")  # Score of the game
# score_rect = score_surf.get_rect(midright=(750,30))


# Enemies

# Snail
snail_frame1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()  # Enemy image - Use "convert_alpha()" in the Enemy
snail_frame2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame1, snail_frame2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

# snail_x_position = 600      # Snail position in a var.
# snail_rect = snail_surface.get_rect(midbottom = (600,300))

# Fly
fly_frame1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()  # Enemy image - Use "convert_alpha()" in the Enemy
fly_frame2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame1, fly_frame2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

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

# test_surface = pygame.Surface((100,200)) # First number is width and Second is height
# test_surface.fill('Red')

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


            # if event.type == pygame.MOUSEBUTTONUP:
            #     print("Release the button to appear this message")

            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     print("Click a button to appear this message")

# Event
            if event.type == obstacle_timer and game_active:
                if randint(0,2):
                    obstacle_rect_list.append(snail_surf.get_rect(midbottom=(randint(900,1100),300)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(midbottom=(randint(900, 1100), 200)))


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

        # pygame.draw.line(screen,"Red", (0,0),pygame.mouse.get_pos(), 10)      It can pick a line of any position I want
        # snail_x_position += -4      # Change the x position of the Snail after each loop - Will make the Enemy "Walk"

        # if snail_x_position < -100:  # This will make the Enemy come back to the value set down there (800), This will happen after the enemy reach -100
        #     snail_x_position = 800

        # screen.blit(snail_surface,(snail_x_position, 250))  # (X,Y) Position of Enemy in game

        # snail_rect.x += -5      # Moves the snail to the right
        #
        # if snail_rect.right <= 0:  # Here we pick the right side of the snail, and compare with "0" (the number I want)
        #     snail_rect.left = 800  # Here the left part of the snail returns to 800

        # screen.blit(snail_surface, snail_rect)


# KeyBoard Input
    #     keys = pygame.key.get_pressed()         # Putting the method in a var
        # if keys[pygame.K_SPACE]:       # Checking if the K_"Button" is pressed, and printing something if it is
        #     player_gravity += -10

# Gravity
        player_gravity += 0.5
        player_rect.y += player_gravity

# Enemies Animation Event
        if event.type == snail_animation_timer:
            if snail_frame_index == 0:
                snail_frame_index = 1
            else:
                snail_frame_index = 0
            snail_surf = snail_frames[snail_frame_index]

        if event.type == fly_animation_timer:
            if fly_frame_index == 0:
                fly_frame_index = 1
            else:
                fly_frame_index = 0
            fly_surf = fly_frames[fly_frame_index]

# Obstacle Movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        if player_rect.bottom >= 300:
            player_rect.bottom = 300
        player_animation()
        screen.blit(player_surface, player_rect)




# Collision
        # if snail_rect.colliderect(player_rect):
        #     game_active = False

        game_active = collision(player_rect,obstacle_rect_list)



        # screen.blit(enemies, (700, 100))

        # player_rect.colliderect(snail_rect)     #  This see the collision between two objects

        # if player_rect.colliderect(snail_rect):    # Python makes the condition False when there is no collision, and when has collision is True
        #     print("collision")


    # Using the mouse to get the collision point
        # mouse_pos = pygame.mouse.get_pos()      # Here we are getting the mouse position

        # Player.rect can be traded for snail.rect and will still work
        # if player_rect.collidepoint(mouse_pos): # Here we use the mouse position when is in contact with the object we want

            # print("Collision")
            # print(pygame.mouse.get_pressed())   # Return condition when the mouse is pressed, booleans.



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





