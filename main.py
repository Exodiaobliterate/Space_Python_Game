import pygame
from pygame import mixer
import Sprite

import sys

#initializes pygames modules for use
pygame.init()
mixer.init()

#the colors of things like the screen and cube
color = (255, 212, 252)
rect_color = (255,0,0)

#the size of the screen display
canvas = pygame.display.set_mode((980, 720), pygame.RESIZABLE)

#the captions of the window for use
pygame.display.set_caption('Space guy')

mixer.music.load("Die.mp3")

x = 200
y = 200

width = 20
height = 20

vel = 10
v = 5
m = 1

BLACK = (0,0,0)
GREEN = (0, 128, 0)

#an image for background if wanted
bg_image_far = pygame.image.load("sprite_Background_far.png").convert_alpha()
bg_image_middle = pygame.image.load("sprite_Background_middle.png").convert_alpha()
bg_image_close = pygame.image.load("sprite_Background_close.png").convert_alpha()

Sprite_Sheet = pygame.image.load("Basic Guy.png").convert_alpha()
Sprite_Sheet = Sprite.SpriteSheet(Sprite_Sheet)

platform1 = pygame.image.load("Platform.png.png").convert_alpha()
platform1_scaled = pygame.transform.scale(platform1, (300, 32))
platform1_rect = pygame.Rect(0, 355, platform1_scaled.get_width(), platform1_scaled.get_height())

platform2 = pygame.image.load("Platform.png.png").convert_alpha()
platform2_scaled = pygame.transform.scale(platform2, (300, 32))
platform2_rect = pygame.Rect(450, 355, platform2_scaled.get_width(), platform2_scaled.get_height())

platform3 = pygame.image.load("Platform.png.png").convert_alpha()
platform3_scaled = pygame.transform.scale(platform3, (150, 32))
platform3_rect = pygame.Rect(450, 355, platform3_scaled.get_width(), platform3_scaled.get_height())

platform4 = pygame.image.load("Platform.png.png").convert_alpha()
platform4_scaled = pygame.transform.scale(platform4, (150, 32))
platform4_rect = pygame.Rect(450, 355, platform4_scaled.get_width(), platform4_scaled.get_height())

platform5 = pygame.image.load("Platform.png.png").convert_alpha()
platform5_scaled = pygame.transform.scale(platform5, (150, 32))
platform5_rect = pygame.Rect(450, 355, platform5_scaled.get_width(), platform5_scaled.get_height())

gateway = pygame.image.load("Portal_Gateway-1.png.png").convert_alpha()
gateway_scaled = pygame.transform.scale(gateway, (200, 225))
gateway_rect = pygame.Rect(550, 130, gateway_scaled.get_width(), gateway_scaled.get_height())

Exit_Gateway = pygame.image.load("Start-1.png.png").convert_alpha()
Exit_Gateway_scaled = pygame.transform.scale(Exit_Gateway, (150, 175))
Exit_Gateway_rect = pygame.Rect(125, 325, Exit_Gateway_scaled.get_width(), Exit_Gateway_scaled.get_height() - 155)

DeathI = pygame.image.load("DebugDie.png")
DeathIscaled = pygame.transform.scale(DeathI, (1920, 50))
DeathRect = pygame.Rect(0, 1080, DeathIscaled.get_width(), DeathIscaled.get_height())

musicgoing = False

def Draw_Bg():
    scaled = pygame.transform.scale(bg_image_far, (980, 720))
    scaled2 = pygame.transform.scale(bg_image_middle, (490, 360))
    scaled3 = pygame.transform.scale(bg_image_close, (490, 360))
    canvas.blit(scaled, (0,0))
    canvas.blit(scaled2, (300,0))
    canvas.blit(scaled3, (300,0))

def Image_Appear():
    print("Active ")
    GleepGlorp = pygame.image.load("Gleeb.png")
    GleepGlorpScaled = pygame.transform.scale(GleepGlorp, (980, 720))
    canvas.blit(GleepGlorpScaled, (0, 0))

def Music(songPath, LoopAmount):
    if not songPath == "":
        mixer.music.load(songPath)
        if not LoopAmount == 0:
            mixer.music.play(LoopAmount)
        else:
            mixer.music.play()
            musicgoing = True
            pygame.time.wait(300)
            musicgoing = False


#creaate animation list
animation_list = []
animation_steps = [4, 4, 38, 19, 27]
action = 0
last_update = pygame.time.get_ticks()
animation_cooldown = 150
frame = 0
step_counter = 0

#the variable telling what level it is
Level = 1
animation_done = False

#moving
CanMove = True

#flipping
isflipped = False

#the bool keeping it running
running = True
jumping = False
istouchingfloor = False

PrevLevel = 0

for animation in animation_steps:
    temp_img_list = []
    for _ in range(animation):
       temp_img_list.append(Sprite_Sheet.get_image(step_counter, 32, 32, 3, BLACK))
       step_counter += 1
    animation_list.append(temp_img_list)

playerPOS = (0, 0)

#the game lop that maeks this all posible
while running:
    pygame.time.delay(10)

    Sprite_sheet_rect = pygame.Rect(x + 30, y - 42, 32, 74)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if CanMove == True:
        if keys[pygame.K_LEFT] and x>-30: #move left
            x -= vel
            if not action == 1:
                action = 1
            print(x)

        if keys[pygame.K_RIGHT] and x < 1920: #move right
            x += vel
            if not action == 1:
                action = 1
            print(x)

        if not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]: #controls idle animation
            action = 0

        if jumping == False: #controls when to fall
            if platform1_rect.colliderect(Sprite_sheet_rect) or platform2_rect.colliderect(Sprite_sheet_rect) or platform3_rect.colliderect(Sprite_sheet_rect) or platform4_rect.colliderect(Sprite_sheet_rect) or platform5_rect.colliderect(Sprite_sheet_rect) or Exit_Gateway_rect.colliderect(Sprite_sheet_rect):
                y = y
                if not istouchingfloor:
                    istouchingfloor = True
            elif not platform1_rect.colliderect(Sprite_sheet_rect) or not platform2_rect.colliderect(Sprite_sheet_rect) or not platform3_rect.colliderect(Sprite_sheet_rect) or not platform4_rect.colliderect(Sprite_sheet_rect) or not platform5_rect.colliderect(Sprite_sheet_rect) or not Exit_Gateway_rect.colliderect(Sprite_sheet_rect)  and jumping == True:
                y += 5
                if istouchingfloor:
                    istouchingfloor = False
            
            if keys[pygame.K_SPACE] and istouchingfloor == True:
                jumping = True

        if jumping: #controls the jump functionality
            F = (1 / 0.25)*m*(v**2) #jump height
            print(F)

            y -= F 
            jumping = False

    if Sprite_sheet_rect.colliderect(gateway_rect):
        if not action == 2:
            action = 2
        CanMove = False
        if frame == 37:
            print("WE HERE!")
            animation_done = True
            if not Level == 4:
                Level += 1
            else:
                Level = 1
    
    if Sprite_sheet_rect.colliderect(DeathRect):
        mixer.music.stop()
        Music("Die.mp3", 0)
        quit()
    elif musicgoing == False and not Sprite_sheet_rect.colliderect(DeathRect):
        mixer.music.stop()
        Music("BackgRound Sound.mp3", 9999)
        musicgoing = True
        
    #update background
    canvas.fill(BLACK)
    
    #update anim
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        frame += 1
        last_update = current_time
        if frame >= len(animation_list[action]):
            frame = 0

    #blits in all the sprites
    Draw_Bg()
    if Level == 1:
        if CanMove == False and animation_done == True:
            platform1_rect.update(0, 355, platform1_scaled.get_width(), platform1_scaled.get_height())
            platform2_rect.update(450, 355, platform2_scaled.get_width(), platform2_scaled.get_height())
            platform3_rect.update(-1000, -1000, platform3_scaled.get_width(), platform3_scaled.get_height())
            platform4_rect.update(-1000, -1000, platform4_scaled.get_width(), platform4_scaled.get_height())
            platform5_rect.update(-1000, -1000, platform5_scaled.get_width(), platform5_scaled.get_height())
            gateway_rect.update(550, 130, gateway_scaled.get_width(), gateway_scaled.get_height())
            Exit_Gateway_rect.update(125, 325, Exit_Gateway_scaled.get_width(), Exit_Gateway_scaled.get_height() - 155)
            if not action == 4:
                frame = 0
            action = 4
            x = 200
            y = 200
            Image_Appear()
            if frame == 26:
                frame = 0
                CanMove = True
                animation_done = False
        canvas.blit(platform1_scaled, (0, 355))
        canvas.blit(platform2_scaled, (450, 355))
        canvas.blit(gateway_scaled, (550, 130))
        canvas.blit(Exit_Gateway_scaled, (125, 180))
    elif Level == 2:
        if CanMove == False and animation_done == True:
            platform1_rect.update(0, 255, platform1_scaled.get_width(), platform1_scaled.get_height())
            platform2_rect.update(900, 355, platform2_scaled.get_width(), platform2_scaled.get_height())
            platform3_rect.update(500, 255, platform3_scaled.get_width(), platform3_scaled.get_height())
            platform4_rect.update(750, 235, platform4_scaled.get_width(), platform4_scaled.get_height())
            platform5_rect.update(1250, 220, platform5_scaled.get_width(), platform5_scaled.get_height())
            gateway_rect.update(1500, 225, gateway_scaled.get_width(), gateway_scaled.get_height())
            Exit_Gateway_rect.update(125, 220, Exit_Gateway_scaled.get_width(), Exit_Gateway_scaled.get_height() - 155)
            if not action == 4:
                frame = 0
            action = 4
            x = 200
            y = 200
            Image_Appear()
            if frame == 26:
                frame = 0
                CanMove = True
                animation_done = False
        canvas.blit(platform1_scaled, (0, 255))
        canvas.blit(platform2_scaled, (900, 355))
        canvas.blit(platform3_scaled, (500, 255))
        canvas.blit(platform4_scaled, (750, 235))
        canvas.blit(platform5_scaled, (1250, 220))
        canvas.blit(gateway_scaled, gateway_rect)
        canvas.blit(Exit_Gateway_scaled, (125, 80))
    elif Level == 3:
        if CanMove == False and animation_done == True:
            platform1_rect.update(0, 255, platform1_scaled.get_width(), platform1_scaled.get_height())
            platform2_rect.update(900, 600, platform2_scaled.get_width(), platform2_scaled.get_height())
            platform3_rect.update(400, 600, platform3_scaled.get_width(), platform3_scaled.get_height())
            platform4_rect.update(750, 600, platform4_scaled.get_width(), platform4_scaled.get_height())
            platform5_rect.update(1250, 750, platform5_scaled.get_width(), platform5_scaled.get_height())
            gateway_rect.update(1250, 725, gateway_scaled.get_width(), gateway_scaled.get_height())
            Exit_Gateway_rect.update(0, 300, Exit_Gateway_scaled.get_width(), Exit_Gateway_scaled.get_height() - 155)
            if not action == 4:
                frame = 0
            action = 4
            x = 200
            y = 200
            Image_Appear()
            if frame == 26:
                frame = 0
                CanMove = True
                animation_done = False
        canvas.blit(platform1_scaled, platform1_rect)
        canvas.blit(platform2_scaled, platform2_rect)
        canvas.blit(platform3_scaled, platform3_rect)
        canvas.blit(platform4_scaled, platform4_rect)
        canvas.blit(platform5_scaled, platform5_rect)
        canvas.blit(gateway_scaled, gateway_rect)
        canvas.blit(Exit_Gateway_scaled, (0, 300))
    elif Level == 4:
        print("End of game")
        quit()
    elif Level == 0:
        Level = PrevLevel
        print("DADO BROKE IT")
    canvas.blit(animation_list[action][frame], (x, y - 65))
    pygame.draw.rect(canvas, GREEN, platform1_rect)
    pygame.draw.rect(canvas, GREEN, platform2_rect)
    pygame.draw.rect(canvas, GREEN, platform3_rect)
    pygame.draw.rect(canvas, GREEN, platform4_rect)
    pygame.draw.rect(canvas, GREEN, platform5_rect)
    pygame.draw.rect(canvas, GREEN, gateway_rect)
    pygame.draw.rect(canvas, GREEN, Exit_Gateway_rect)
    pygame.display.update()