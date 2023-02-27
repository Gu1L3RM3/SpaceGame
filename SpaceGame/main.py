import pygame
from sys import exit
from random import randint,uniform

def laser_update(laser_list,speed=300):
    for rect in laser_list:
        rect.y -=round(speed*dt)
        if rect.bottom <0:
            laser_list.remove(rect)
#movement
def move():
    global ship_rect
    _mouse = pygame.mouse.get_pos()
    ship_rect.center=_mouse 
#shoot
def shoot():
    global laser_list
    #laser_update(laser_list)
    for laser in laser_list:
        display_surface.blit(laser_surf,laser)
def display_score():
    score_text=f'Score:{pygame.time.get_ticks()//1000}'

    text_surf = font.render(score_text,True,WHITE)
    text_rect= text_surf.get_rect(midbottom=(WIDHT/2,HEIGHT-80))
    display_surface.blit(text_surf,text_rect)
    pygame.draw.rect(display_surface,WHITE,text_rect.inflate(30,30),width=8,border_radius=5)


def laser_timer(can_shoot,duration=500):
    if not can_shoot :
        current_time=pygame.time.get_ticks()
        if current_time-shoot_time>duration:
            can_shoot = True
    return can_shoot
#meteor functions 
def meteror_drop():
    global meteor_list
    #laser_update(laser_list)
    for meteor_tuple in meteor_list:
        display_surface.blit(meteor_surf,meteor_tuple[0])

def meteor_update(meteor_list,speed=500):
    for meteor_tuple in meteor_list:
        direction=meteor_tuple[1]
        meteor_rect=meteor_tuple[0]
        meteor_rect.center+=direction*speed*dt
        #rect.y +=round(speed*dt)
        if meteor_rect.top >HEIGHT:
            meteor_list.remove(meteor_tuple)

def collision_ship(meteor_list,ship_rect):
    for meteor_tuple in meteor_list:
        meteor_rect =meteor_tuple[0]
        if ship_rect.colliderect(meteor_rect):
            pygame.quit()
            exit()

def collision_laser(meteor_list,laser_list):

    for meteor_tuple in meteor_list:
        for laser_rect in laser_list:
             meteor_rect=meteor_tuple[0]
             if laser_rect.colliderect(meteor_rect):
                 meteor_list.remove(meteor_tuple)
                 laser_list.remove(laser_rect)
                 explosion_sound.play()







pygame.init()


#Constants
WIDHT=1200
HEIGHT=600
WHITE=(255,255,255)
BLACK=(0,0,0)
SHIP='graphics\ship.png'
METEOR='graphics\meteor.png'
BACKGROUND='graphics\\background.png'
FONTE='graphics\subatomic.ttf'
LASER='graphics\laser.png'
MUSIC='sounds\music.wav'
LASER_MUSIC='sounds\laser.ogg'
EXPLOSION='sounds\explosion.wav'



display_surface=pygame.display.set_mode((WIDHT,HEIGHT))
pygame.display.set_caption('SpaceGame')
time=pygame.time.Clock()

#importing images 

#image ship
ship_surf=pygame.image.load(SHIP).convert_alpha()
ship_rect=ship_surf.get_rect(center=(600,300))

#image background
background_surf=pygame.image.load(BACKGROUND).convert()

#image laser
laser_surf=pygame.image.load(LASER).convert_alpha()
laser_list=[]
#laser_rect=laser_surf.get_rect(midbottom = ship_rect.midtop)

#image meteor
meteor_surf=pygame.image.load(METEOR).convert_alpha()
meteor_list=[]

#import text 
font =pygame.font.Font(FONTE,50)

#import music
laser_sound=pygame.mixer.Sound(LASER_MUSIC)
explosion_sound=pygame.mixer.Sound(EXPLOSION)
background_music=pygame.mixer.Sound(MUSIC)
background_music.play(loops=-1)

can_shoot=True
shoot_time=None

#meteor timer 
meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer,300)





        





while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        #if event.type == pygame.MOUSEMOTION:
         #   ship_rect.center=event.pos
        
        if event.type == pygame.MOUSEBUTTONDOWN and can_shoot:
            
            laser_rect=laser_surf.get_rect(midbottom = ship_rect.midtop)
            laser_list.append(laser_rect)
            can_shoot=False
            shoot_time=pygame.time.get_ticks()

            laser_sound.play()
        if event.type ==meteor_timer:
            
            meteor_rect=meteor_surf.get_rect(center=(randint(-100,WIDHT+100),randint(-100,-50)))
            
            direction=pygame.math.Vector2(uniform(-0.5,0.5),1)
            
            meteor_list.append((meteor_rect,direction))

    
  
    collision_laser(meteor_list,laser_list)
    collision_ship(meteor_list,ship_rect)
    dt=time.tick(120)/1000
     # mouse input
    move()
    #laser_rect.y-=round(200*dt)
        
    #draw images 
    display_surface.blit(background_surf,(0,0))
    display_score()
    display_surface.blit(ship_surf,ship_rect)
    #display_surface.blit(laser_surf,laser_rect)
    #if ship_rect.y > 0 :
       # ship_rect.y-=4
    #for loop that draw the laser surface where the rects are 
    laser_update(laser_list)
    can_shoot=laser_timer(can_shoot,300)

    meteor_update(meteor_list)

    shoot()
    meteror_drop()

    

    #display_surface.blit(text_surf,(500,200))

   
   
    
    




    pygame.display.flip()
    

