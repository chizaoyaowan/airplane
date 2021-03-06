import pygame
import sys
from pygame.locals import *
from random import *
import traceback
import myplane
import enemy
import bullet
import supply
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
White=(255,255,255)


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

def inc_speed(target,inc):
    for each in target:
        each.speed += inc

def me_speed(target,inc):
        target.speed += inc

def inc_energy(target,inc):
    for each in target: 
        each.energy += inc

def main():

    #用于防止重复打开文档
    recorded = False
    
    #播放背景音乐
    pygame.mixer.music.play(-1)
    
    #生成我方飞机
    me = myplane.MyPlane(bg_size)

    #生成子弹
    bullet1 =[]
    bullet1_index =0
    bullet1_num =4
    for i in range(bullet1_num):
        bullet1.append(bullet.Bullet1(me.rect.midtop))
    
    #生命数量
    life_image =pygame.image.load("ui/shoot/hero_life.png").convert_alpha()
    life_rect=life_image.get_rect()
    life_num =3
    
    
    #生成超级子弹
    bullet2 =[]
    bullet2_index =0
    bullet2_num =8
    for i in range(bullet2_num//2):
        bullet2.append(bullet.Bullet2((me.rect.centerx - 33,me.rect.centery)))
        bullet2.append(bullet.Bullet2((me.rect.centerx + 30,me.rect.centery)))


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

    #记录得分
    score = 0
    score_font = pygame.font.Font("font/font.ttf",36)

    #设置难度级别
    level = 1

    #暂停
    pause = False
    game_pause_nor_image=pygame.image.load("ui/shoot/game_pause_nor.png").convert_alpha()
    game_pause_pressed_image=pygame.image.load("ui/shoot/game_pause_pressed.png").convert_alpha()
    game_resume_nor_image=pygame.image.load("ui/shoot/game_resume_nor.png").convert_alpha()
    game_resume_pressed_image=pygame.image.load("ui/shoot/game_resume_pressed.png").convert_alpha()
    pause_rect = game_pause_nor_image.get_rect()
    pause_rect.left,pause_rect.top =width - pause_rect.width -10 ,10
    pause_image = game_pause_nor_image
    
    #全屏炸弹
    bomb_image = pygame.image.load("ui/shoot/bomb.png").convert_alpha()
    bomb_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font("font/font.ttf",48)
    bomb_num =3

    #每15秒发一个补给包
    bullet_supply =supply.bullet_supply(bg_size)
    bomb_supply =supply.bomb_supply(bg_size)
    supply_time = USEREVENT
    pygame.time.set_timer(supply_time,20*1000)

    #超级子弹计时器
    double_bullet_time = USEREVENT + 1

    #解除无敌计时器
    invincible_time = USEREVENT +2
    
    
    #标志是否使用超级子弹
    is_double_bullet = False
    
    #绘制结束图片
    gameover_font =pygame.font.Font("font/font.ttf",48)
    again_image=pygame.image.load("ui/shoot/game_again.png").convert_alpha()
    again_rect=again_image.get_rect()
    gameover_image=pygame.image.load("ui/shoot/game_over.png").convert_alpha()
    gameover_rect=gameover_image.get_rect()
    #延时
    delay=100
    
    running =True

    clock=pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            #暂停
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and pause_rect.collidepoint(event.pos):
                    pause = not pause
                    if pause:
                        pygame.time.set_timer(supply_time,0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        pygame.time.set_timer(supply_time,20*1000)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()
            
            elif event.type == MOUSEMOTION:
                if pause_rect.collidepoint(event.pos):
                    if pause:
                        pause_image =game_resume_pressed_image
                    else:
                        pause_image =game_pause_pressed_image
                else:
                    if pause:
                        pause_image =game_resume_nor_image
                    else:
                        pause_image =game_pause_nor_image
            #炸弹
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        use_bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.active = False
            #随机生成补给
            elif event.type == supply_time:
                if choice([True,False]):
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()
            #结束超级子弹
            elif event.type == double_bullet_time:
                is_double_bullet = False
                pygame.time.set_timer(double_bullet_time,0)
            #结束无敌
            elif event.type == invincible_time:
                me.invincible =False
                pygame.time.set_timer(invincible_time,0)

        #提升难度
        #难度2
        if level == 1 and score >5000:
            level =2
            achievement_sound.play()
            #增加敌机
            add_small_enemies(small_enemies,enemies,2)
            add_mid_enemies(mid_enemies,enemies,3)
            add_big_enemies(big_enemies,enemies,1)
            #提升速度
            inc_speed(mid_enemies,1)
            inc_energy(mid_enemies,1)
            me_speed(me,1)
        #难度3
        if level == 2 and score >20000:
            level =3
            achievement_sound.play()
            #增加敌机
            add_small_enemies(small_enemies,enemies,1)
            #add_mid_enemies(mid_enemies,enemies,1)
            add_big_enemies(big_enemies,enemies,1)
            #提升速度
            inc_speed(big_enemies,0.5)
            inc_energy(big_enemies,2)
            me_speed(me,1)
        #难度4
        if level == 3 and score >35000:
            level =4
            achievement_sound.play()
            #增加敌机
            add_small_enemies(small_enemies,enemies,3)
            add_mid_enemies(mid_enemies,enemies,3)
            add_big_enemies(big_enemies,enemies,2)
            #提升速度
            inc_speed(small_enemies,1)
            inc_energy(mid_enemies,2)
        #难度5
        if level == 4 and score >60000:
            level =5
            achievement_sound.play()
            #增加敌机
            add_small_enemies(small_enemies,enemies,2)
            add_mid_enemies(mid_enemies,enemies,4)
            add_big_enemies(big_enemies,enemies,1)
            #提升速度
            #inc_speed(small_enemies,1)            
            #inc_energy(big_enemies,1)
            
                
        #绘制背景
        screen.blit(background,(0,0))
        

        if life_num and not pause:                              

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
            #绘制炸弹补给
            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image,bomb_supply.rect)            
                if pygame.sprite.collide_mask(bomb_supply,me):
                    get_bomb_sound.play()
                    bomb_num += 1
                    bomb_supply.active =False

            #绘制超级子弹补给
            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image,bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply,me):
                    get_double_laser_sound.play()
                    is_double_bullet = True
                    pygame.time.set_timer(double_bullet_time,10*1000)
                    bullet_supply.active =False       
            

            #绘制大飞机
            if level >= 2:
                for each in big_enemies:
                    if each.active:
                        each.move()
                        if switch_image:
                            screen.blit(each.image1,each.rect)
                        else:
                            screen.blit(each.image2,each.rect)

                        #绘制被打到的画面
                        if each.hit:
                            screen.blit(each.hit_image,each.rect)
                            if not(delay % 10):
                                each.hit = False
                        
                        #绘制血槽
                        pygame.draw.line(screen,Black,\
                                         (each.rect.left,each.rect.top +2),\
                                         (each.rect.right,each.rect.top +2),\
                                         2)
                        #当生命大于20%显示绿色，小于显示红色
                        energy_remin =each.energy / enemy.bigenemy.energy
                        if energy_remin > 0.2:
                            energy_color = Green
                        else:
                            energy_color = Red
                        pygame.draw.line(screen,energy_color,\
                                         (each.rect.left,each.rect.top + 2),\
                                         (each.rect.left + each.rect.width*energy_remin,\
                                          each.rect.top + 2),2)
        
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
                                score += 500
                                each.reset()
                    
                
            #绘制中飞机
            for each in mid_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image,each.rect)
                    #绘制被打到的画面
                    if each.hit:
                        screen.blit(each.hit_image,each.rect)
                        if not(delay % 10):
                            each.hit = False

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
                            score += 200
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
                            score +=50
                            each.reset()
            #我方飞机碰撞检测
            enemies_down =pygame.sprite.spritecollide(me,enemies,False,pygame.sprite.collide_mask)
            if enemies_down and not me.invincible:
                me.active =False
                for e in enemies_down:
                    e.active =False

            #绘制我方飞机
            if me.active:
                if switch_image:
                    screen.blit(me.image1,me.rect)
                else:
                    screen.blit(me.image2,me.rect)
                if not(delay % 100):
                    score += 50
            else:
                    #毁灭
                    if not(delay % 4):
                        if me_destroy_index == 0:
                            out_porp_sound.play()
                        screen.blit(me.destroy_image[me_destroy_index],me.rect)
                        me_destroy_index =(me_destroy_index +1)%4
                        if me_destroy_index == 0:
                            life_num -= 1
                            me.reset()
                            pygame.time.set_timer(invincible_time,3 * 1000)
                            

            #绘制剩余生命数
            if life_num:
                for i in range(life_num):
                    screen.blit(life_image,\
                                (width -10 - (i+1)*life_rect.width,\
                                 height-10-life_rect.height))
            #绘制分数                   
            score_text = score_font.render("Score: %s" %str(score),True,White)
            screen.blit(score_text,(10,5))

            #绘制子弹
            if not(delay % 20):
                bullet_sound.play()
                if is_double_bullet:
                    bullets=bullet2
                    bullets[bullet2_index].reset((me.rect.centerx - 33,me.rect.centery))
                    bullets[bullet2_index+1].reset((me.rect.centerx + 30,me.rect.centery))
                    bullet2_index =(bullet2_index+2) % bullet2_num
                    
                else:
                    bullets=bullet1
                    bullets[bullet1_index].reset(me.rect.midtop)
                    bullet1_index =(bullet1_index+1) % bullet1_num
                
                
                

            #子弹碰撞检测
            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image,b.rect)
                    enemy_hit =pygame.sprite.spritecollide(b,\
                                                           enemies,False,\
                                                           pygame.sprite.collide_mask)
                    if enemy_hit:
                        b.active =False
                        for e in enemy_hit:
                            e.hit = True
                            if e in mid_enemies or e in big_enemies:
                                e.energy -=1
                                if e.energy == 0:
                                    e.active = False
                            else:
                                e.active =False

        
        #绘制游戏结束画面
        elif life_num == 0:
            
            #停止背景音乐
            pygame.mixer.music.stop()
            #停止音效
            pygame.mixer.stop()
            #停止发放补给
            pygame.time.set_timer(supply_time,0)

            if not recorded:
                recorded =True
                #读取历史最高分
                with open("record.txt","r") as f:
                    record_score =int(f.read())
                #如果玩家高于历史分，则存档
                if score> record_score:
                    with open("record.txt","w") as f:
                        f.write(str(score))
            # 绘制结束画面
            record_score_text = score_font.render("Best : %d" % record_score, True, (255, 255, 255))
            screen.blit(record_score_text, (50, 50))
            
            gameover_text1 = gameover_font.render("Your Score", True, (255, 255, 255))
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = \
                                 (width - gameover_text1_rect.width) // 2, height // 3
            screen.blit(gameover_text1, gameover_text1_rect)
            
            gameover_text2 = gameover_font.render(str(score), True, (255, 255, 255))
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = \
                                 (width - gameover_text2_rect.width) // 2, \
                                 gameover_text1_rect.bottom + 10
            screen.blit(gameover_text2, gameover_text2_rect)

            again_rect.left, again_rect.top = \
                             (width - again_rect.width) // 2, \
                             gameover_text2_rect.bottom + 50
            screen.blit(again_image, again_rect)

            gameover_rect.left, gameover_rect.top = \
                                (width - again_rect.width) // 2, \
                                again_rect.bottom + 10
            screen.blit(gameover_image, gameover_rect)

            # 检测用户的鼠标操作
            # 如果用户按下鼠标左键
            if pygame.mouse.get_pressed()[0]:
                # 获取鼠标坐标
                pos = pygame.mouse.get_pos()
                # 如果用户点击“重新开始”
                if again_rect.left < pos[0] < again_rect.right and \
                   again_rect.top < pos[1] < again_rect.bottom:
                    # 调用main函数，重新开始游戏
                    main()
                # 如果用户点击“结束游戏”            
                elif gameover_rect.left < pos[0] < gameover_rect.right and \
                     gameover_rect.top < pos[1] < gameover_rect.bottom:
                    # 退出游戏
                    pygame.quit()
                    sys.exit()

        #绘制暂停按钮
        screen.blit(pause_image,pause_rect)

        #绘制炸弹
        bomb_text = bomb_font.render("x %d "%bomb_num,True,White)
        text_rect = bomb_text.get_rect()
        screen.blit(bomb_image,(10,height -10 -bomb_rect.height))
        screen.blit(bomb_text,(20 + bomb_rect.width,height -5 -text_rect.height))


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
