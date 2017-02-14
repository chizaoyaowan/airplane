import pygame
import sys
from pygame.locals import *
from random import *
import traceback
import myplane
import enemy
import bullet
#初始化
pygame.init()
pygame.mixer.init()

#指定窗口大小
bg_size=(width,height)=(480,700)
screen=pygame.display.set_mode(bg_size)

pygame.display.set_caption("飞机大战")
background =pygame.image.load("ui/shoot_background/background.png").convert()

Black=(0,0,0)
Green=(0,255,0)
Red=(255,0,0)


#加载音乐
pygame.mixer.music.load("music/bg.ogg")
pygame.mixer.music.set_volume(0.1)
achievement_sound=pygame.mixer.Sound("music/achievement.wav")
achievement_sound.set_volume(0.2)
big_spaceship_flying_sound=pygame.mixer.Sound("music/big_spaceship_flying.wav")
big_spaceship_flying_sound.set_volume(0.2)
bullet_sound=pygame.mixer.Sound("music/bullet.wav")
bullet_sound.set_volume(0.2)
button_sound=pygame.mixer.Sound("music/button.wav")
button_sound.set_volume(0.2)
enemy1_sound=pygame.mixer.Sound("music/enemy1_down.wav")
enemy1_sound.set_volume(0.2)
enemy2_sound=pygame.mixer.Sound("music/enemy2_down.wav")
enemy2_sound.set_volume(0.2)
enemy3_sound=pygame.mixer.Sound("music/enemy3_down.wav")
enemy3_sound.set_volume(0.2)
game_over_sound=pygame.mixer.Sound("music/game_over.wav")
game_over_sound.set_volume(0.2)
get_bomb_sound=pygame.mixer.Sound("music/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_double_laser_sound=pygame.mixer.Sound("music/get_double_laser.wav")
get_double_laser_sound.set_volume(0.2)
out_porp_sound=pygame.mixer.Sound("music/out_porp.wav")
out_porp_sound.set_volume(0.2)
use_bomb_sound=pygame.mixer.Sound("music/use_bomb.wav")
use_bomb_sound.set_volume(0.2)

def add_small_enemies(Group1,Group2,num):
    for i in range(num):
        e1 = enemy.smallenemy(bg_size)
        Group1.add(e1)
        Group2.add(e1)

def add_mid_enemies(Group1,Group2,num):
    for i in range(num):
        e2 = enemy.midenemy(bg_size)
        Group1.add(e2)
        Group2.add(e2)

def add_big_enemies(Group1,Group2,num):
    for i in range(num):
        e3 = enemy.bigenemy(bg_size)
        Group1.add(e3)
        Group2.add(e3)    

def main():

    #播放背景音乐
    pygame.mixer.music.play()

    #生成我方飞机
    me =myplane.MyPlane(bg_size)

    #生成子弹
    bullet1 =[]
    bullet1_index =0
    bullet1_num =2
    for i in range(bullet1_num):
        bullet1.append(bullet.Bullet1(me.rect.midtop))

    #生成敌方飞机
    enemies =pygame.sprite.Group()

    #生成敌方小飞机
    small_enemies =pygame.sprite.Group()
    add_small_enemies(small_enemies,enemies,15)

    #生成敌方中飞机
    mid_enemies =pygame.sprite.Group()
    add_mid_enemies(mid_enemies,enemies,4)

    #生成敌方中飞机
    big_enemies =pygame.sprite.Group()
    add_big_enemies(big_enemies,enemies,2)

    #中弹图片索引
    e1_destroy_index=0
    e2_destroy_index=0
    e3_destroy_index=0
    me_destroy_index=0

    #切换飞机图片
    switch_image=True

    #延时
    delay=100
    
    running =True

    clock=pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        #检测键盘操作
        key_pressed =pygame.key.get_pressed()
        if key_pressed[K_w] or key_pressed[K_UP]:
            me.moveup()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            me.movedown()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            me.moveleft()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            me.moveright()

        #绘制背景
        screen.blit(background,(0,0))

        #绘制大飞机
        for each in big_enemies:
            if each.active:
                each.move()
                if switch_image:
                    screen.blit(each.image1,each.rect)
                else:
                    screen.blit(each.image2,each.rect)
                #绘制血槽
                pygame.draw.line(screen,Black,\
                                 (each.rect.left,each.rect.top - 5),\
                                 (each.rect.right,each.rect.top -5),\
                                 2)
                #当生命大于20%显示绿色，小于显示红色
                energy_remin =each.energy / enemy.bigenemy.energy
                if energy_remin > 0.2:
                    energy_color = Green
                else:
                    energy_color = Red
                pygame.draw.line(screen,energy_color,\
                                 (each.rect.left,each.rect.top - 5),\
                                 (each.rect.left + each.rect.width*energy_remin,\
                                  each.rect.top - 5),2)
    
                #播放大飞机音效
                if each.rect.bottom > -50:
                    big_spaceship_flying_sound.play(-1)
            else:
                #毁灭
                if not(delay % 6):
                    if e3_destroy_index == 0:
                        enemy3_sound.play()
                    screen.blit(each.destroy_image[e3_destroy_index],each.rect)
                    e3_destroy_index =(e3_destroy_index +1)%6
                    if e3_destroy_index == 0:
                        big_spaceship_flying_sound.stop()
                        each.reset()
                
            
        #绘制中飞机
        for each in mid_enemies:
            if each.active:
                each.move()
                screen.blit(each.image,each.rect)

                #绘制血槽
                pygame.draw.line(screen,Black,\
                                 (each.rect.left,each.rect.top - 5),\
                                 (each.rect.right,each.rect.top -5),\
                                 2)
                #当生命大于20%显示绿色，小于显示红色
                energy_remin =each.energy / enemy.midenemy.energy
                if energy_remin > 0.2:
                    energy_color = Green
                else:
                    energy_color = Red
                pygame.draw.line(screen,energy_color,\
                                 (each.rect.left,each.rect.top - 5),\
                                 (each.rect.left + each.rect.width*energy_remin,\
                                  each.rect.top - 5),2)
            else:
                #毁灭
                if not(delay % 4):
                    if e2_destroy_index == 0:
                        enemy2_sound.play()
                    screen.blit(each.destroy_image[e2_destroy_index],each.rect)
                    e2_destroy_index =(e2_destroy_index +1)%4
                    if e2_destroy_index == 0:
                        each.reset()   
            
        #绘制小飞机
        for each in small_enemies:
            if each.active:
                each.move()
                screen.blit(each.image,each.rect)
            else:
                #毁灭
                if not(delay % 4):
                    if e1_destroy_index == 0:
                        enemy1_sound.play()
                    screen.blit(each.destroy_image[e1_destroy_index],each.rect)
                    e1_destroy_index =(e1_destroy_index +1)%4
                    if e1_destroy_index == 0:
                        each.reset()
        #我方飞机碰撞检测
        enemies_down =pygame.sprite.spritecollide(me,enemies,False,pygame.sprite.collide_mask)
        if enemies_down:
            me.active =False
            for e in enemies_down:
                e.active =False

        #绘制我方飞机
        if me.active:
            if switch_image:
                screen.blit(me.image1,me.rect)
            else:
                screen.blit(me.image2,me.rect)
        else:
                #毁灭
                if not(delay % 4):
                    if me_destroy_index == 0:
                        out_porp_sound.play()
                    screen.blit(me.destroy_image[me_destroy_index],me.rect)
                    me_destroy_index =(me_destroy_index +1)%4
                    if me_destroy_index == 0:
                        me.reset()  
        #绘制子弹
        if not(delay % 20):
            bullet1[bullet1_index].reset(me.rect.midtop)
            bullet1_index =(bullet1_index+1) % bullet1_num
            

        #子弹碰撞检测
        for b in bullet1:
            if b.active:
                b.move()
                screen.blit(b.image,b.rect)
                enemy_hit =pygame.sprite.spritecollide(b,\
                                                       enemies,False,\
                                                       pygame.sprite.collide_mask)
                if enemy_hit:
                    b.active =False
                    for e in enemy_hit:
                        if e in mid_enemies or e in big_enemies:
                            e.energy -=1
                            if e.energy == 0:
                                e.active = False
                        else:
                            e.active =False
                    
            
        #切换图片
        if not (delay % 10):
            switch_image = not  switch_image
        delay -=1
        if  delay == 0:
            delay = 100

        #绘制屏幕
        pygame.display.flip()

        #设置帧率
        clock.tick(120)
            
if __name__ =="__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
