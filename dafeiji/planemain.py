import pygame
import sys
import traceback
from pygame.locals import *
import random
import myplane
import enemy
import bullet
import supply


pygame.init()
pygame.mixer.init()

bg_size = width, height = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("飞机大战---蛋疼的废材")

background = pygame.image.load("imagess/me1.png").convert()   #背景非透明
bg_rect = background.get_rect()

BLACK = (0, 0, 0)
GREEN = (0, 225, 0)
RED = (225, 0, 0)
WHITE = (0, 0, 0)

# 载入游戏音乐音乐
pygame.mixer.music.load("sound/house_lo.wav")
pygame.mixer.music.set_volume(0.1)  # 音量
enemy1_die_sound = pygame.mixer.Sound("sound/enemy1.wav")  # 小敌机阵亡
enemy1_die_sound.set_volume(0.2)
hero_sound_2 = pygame.mixer.Sound("sound/hero1.wav")  # 英雄阵亡
hero_sound_2.set_volume(0.2)
enemy3_fly_sound = pygame.mixer.Sound("sound/enemy3c.wav")  # 大飞机飞行
enemy3_fly_sound.set_volume(0.2)
enemy3_die_sound = pygame.mixer.Sound("sound/enemy3d.wav")  # 大飞机阵亡
enemy3_die_sound.set_volume(0.2)
enemy2_die_sound = pygame.mixer.Sound("sound/enemy2.wav")  # 中飞机阵亡
enemy2_die_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")  # 难度升级
upgrade_sound.set_volume(0.2)
bomb_sound = pygame.mixer.Sound("sound/zhadan.wav")  # 全屏炸弹
bomb_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound("sound/whiff.wav")  # 补给发放
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("sound/chibuji.wav") #吃到补给
get_bomb_sound.set_volume(0.2)

def add_small_enemies(group1, group2, num):     #创建小飞机组
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

def add_mid_enemies(group1, group2, num):           #创建中飞机组
    for i in range(num):
        e2 = enemy.MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)

def add_big_enemies(group1, group2, num):           #创建大飞机组
    for i in range(num):
        e3 = enemy.BigEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)

def inc_speed(target, inc):         #根据难度提升敌机速度
    for each in target:
        each.speed += inc


def main():
    level = 1  # 设置难度级别
    pygame.mixer.music.play(-1)  # 背景音乐

    score = 0               # 统计得分情况
    score_font = pygame.font.Font("ziti/segoeuii.ttf", 36)

    paused = False          ##是否暂停
    pause_nor_image = pygame.image.load("imagess/pause_nor.png").convert_alpha()
    pause_pressed_image = pygame.image.load("imagess/pause_pressed.png").convert_alpha()
    resume_nor_image = pygame.image.load("imagess/resume_nor.png").convert_alpha()
    resume_pressed_image = pygame.image.load("imagess/resume_pressed.png").convert_alpha()
    pause_rect = pause_nor_image.get_rect()
    pause_rect.right, pause_rect.top = width - 10, 10
    pause_image = pause_nor_image

    #全屏炸弹个数显示
    bomb_image = pygame.image.load("imagess/bomb.png")
    bomb_rect = bomb_image.get_rect()
    bomb_fount = pygame.font.Font("ziti/segoeuii.ttf", 36)
    bomb_num = 3
    # 英雄剩余生命
    hero_image = pygame.image.load("imagess/hero3.png").convert_alpha()
    hero_rect = hero_image.get_rect()
    myplane_num = 3

    #每30秒补给包定时器
    bullet_supply = supply.Bullet_supply(bg_size)
    bomb_supply = supply.Bomb_supply(bg_size)
    SUPPLY_TIME = USEREVENT
    pygame.time.set_timer(SUPPLY_TIME, 30*1000)

    #超级子弹定时器
    DOUBLE_TIME = USEREVENT + 1
    is_double_bullet = False
    #复活3秒无敌模式定时器
    LNVINCIBLE_TIME = USEREVENT + 2
    lnvincible_mode = False

    #生成我方飞机
    me = myplane.MyPlane(bg_size)
    #生成敌机精灵
    enemies = pygame.sprite.Group()
    #生成小型飞机
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemies, 20)
    #生成中型飞机
    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 10)
    #生成大型飞机
    big_enemies = pygame.sprite.Group()
    add_big_enemies(big_enemies, enemies, 5)
    #生成子弹

    bullet_active = True    #允许发射子弹
    bullet1 = []
    bullet1_index = 0
    BULLET1_NUM = 4
    for i in range(BULLET1_NUM):
        bullet1.append(bullet.Bullet1(me.rect.midtop))
    bullets = bullet1
    #生成超级子弹
    bullet2 = []
    bullet2_index = 0
    BULLET2_NUM = 8
    for i in range(BULLET2_NUM//2):
        bullet2.append(bullet.Bullet2((me.rect.centerx-33, me.rect.centery)))   #这里只需传入一个参数
        bullet2.append(bullet.Bullet2((me.rect.centerx+33, me.rect.centery)))

    #中弹图片索引
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0

    # 用于切换英雄飞行图片
    switch_image = True
    delay = 100
    #用于阻止重复打开记录文件
    recorded = False

    #结束游戏画面
    restart_image = pygame.image.load("imagess/restart.png").convert_alpha()         #重新开始图片
    restart_rect = restart_image.get_rect()
    restart_rect.centerx = width/2
    restart_rect.centery = height/2
    gameover_image = pygame.image.load("imagess/gameover.png").convert_alpha()       #游戏结束图片
    gameover_rect = gameover_image.get_rect()
    gameover_rect.centerx = width/2
    gameover_rect.centery = height/2 + 80


    clock = pygame.time.Clock()
    """主循环"""
    while True:
        screen.blit(background, bg_rect)     #绘制背景
        screen.blit(background, (bg_rect.x, bg_rect.y - 700))  # 绘制背景
        if bg_rect.y >= 700:
            bg_rect.y = 0


        for event in pygame.event.get():  # 事件监听
            if event.type ==pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 :                          #左键单击
                    if pause_rect.collidepoint(event.pos):
                        paused = not paused
                        if paused:
                            pygame.mixer.music.pause()
                            pygame.mixer.pause()
                            pygame.time.set_timer(SUPPLY_TIME, 0)
                        else:
                            pygame.mixer.music.unpause()
                            pygame.mixer.unpause()
                            pygame.time.set_timer(SUPPLY_TIME, 30*1000)
                    elif gameover_rect.collidepoint(event.pos):     #退出游戏
                        if myplane_num <= 0:
                            pygame.quit()
                            sys.exit()
                    elif restart_rect.collidepoint(event.pos):      #重新开始
                        if myplane_num<= 0:
                            main()

            elif event.type ==MOUSEMOTION:              #鼠标有动作
                if pause_rect.collidepoint(event.pos):      #鼠标放在暂停区域
                    if paused:
                        pause_image = resume_pressed_image
                    else:
                        pause_image = pause_pressed_image

                else:                                       # 鼠标不在暂停区域
                    if paused:
                        pause_image = resume_nor_image
                    else:
                        pause_image = pause_nor_image

            elif event.type == KEYDOWN:
                if event.key == K_SPACE:         #如果按下空格键：
                    if bomb_num:
                        bomb_num -= 1           #投放全屏炸弹
                        bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom > -10:
                                each.active = False

            elif event.type == SUPPLY_TIME:         #发放补给
                supply_sound.play()
                if random.choice([True, False]):    #这里要写成字典
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()

            elif event.type == DOUBLE_TIME:
                is_double_bullet = False
                pygame.time.set_timer(DOUBLE_TIME, 0)

            elif event.type == LNVINCIBLE_TIME:
                lnvincible_mode = False


        #根据得分情况增加游戏难度
        if level == 1 and score >= 500:
            level = 2
            upgrade_sound.play()
            add_small_enemies(small_enemies, enemies, 6)
            add_mid_enemies(mid_enemies, enemies, 4)
            add_big_enemies(big_enemies, enemies, 2)

        elif level == 2 and score >= 3000:
            level = 3
            upgrade_sound.play()
            add_small_enemies(small_enemies, enemies, 8)
            add_mid_enemies(mid_enemies, enemies, 6)
            add_big_enemies(big_enemies, enemies, 3)
            # 提升敌机速度
            inc_speed(small_enemies, 1)

        elif level == 3 and score >= 5000:
            level = 4
            upgrade_sound.play()
            add_small_enemies(small_enemies, enemies, 9)
            add_mid_enemies(mid_enemies, enemies, 7)
            add_big_enemies(big_enemies, enemies, 4)
            # 提升敌机速度
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)

        elif level == 4 and score >= 10000:
            level = 5
            upgrade_sound.play()
            add_small_enemies(small_enemies, enemies, 10)
            add_mid_enemies(mid_enemies, enemies, 8)
            add_big_enemies(big_enemies, enemies, 4)
            # 提升敌机速度
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)

        elif level == 5 and score >= 20000:
            level = 6
            upgrade_sound.play()
            add_small_enemies(small_enemies, enemies, 12)
            add_mid_enemies(mid_enemies, enemies, 10)
            add_big_enemies(big_enemies, enemies, 5)
            # 提升敌机速度
            inc_speed(small_enemies, 1)
            inc_speed(mid_enemies, 1)
            inc_speed(big_enemies, 1)

        #绘制游戏难度
        pygame.draw.line(screen, BLACK, (5, 600), (5, 100), 2)
        pygame.draw.line(screen, RED, (5, 600), (5, 600-100*(level-1)), 2)


        if not paused and myplane_num > 0:
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_UP]:  # 上
                me.movup()
            elif keys_pressed[pygame.K_DOWN]:  # 下
                me.movdown()
            elif keys_pressed[pygame.K_LEFT]:  # 左
                me.movleft()
            elif keys_pressed[pygame.K_RIGHT]:  # 右
                me.movright()

            bg_rect.y += 1      #背景图片运动

            #每10针发射一颗子弹
            if not(delay % 15):
                if is_double_bullet:
                    bullets = bullet2
                    bullet2[bullet2_index].reset((me.rect.centerx-33, me.rect.centery))
                    bullet2[bullet2_index + 1].reset((me.rect.centerx+33, me.rect.centery))
                    bullet2_index = (bullet2_index + 2) % BULLET1_NUM

                else:
                    bullets = bullet1
                    bullet1[bullet1_index].reset(me.rect.midtop)
                    bullet1_index = (bullet1_index + 1) % BULLET1_NUM

            #检测子弹是否击中敌机
            for b in bullets:
                if b.active:
                    b.mov()
                    if bullet_supply:
                        screen.blit(b.image, b.rect)
                    else:
                        screen.blit(b.image, b.rect)
                    enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                    if enemy_hit:
                        b.active = False
                        for e in enemy_hit:
                            if e in mid_enemies or e in big_enemies:
                                e.energy -= 1
                                if e.energy <= 0:
                                    e.active = False
                            else:
                                e.active = False

            #绘制大型敌机
            for each in big_enemies:
                if each.active:
                    each.move()
                    if switch_image:
                        screen.blit(each.image1, each.rect)
                    else:
                        screen.blit(each.image2, each.rect)

                    #绘制大飞机血槽
                    pygame.draw.line(screen, BLACK, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.right, each.rect.top - 5), \
                                     2)
                    # 生命大于30%显示绿色血条，否则为红色
                    energy_remain = each.energy / enemy.BigEnemy.energy
                    if energy_remain > 0.2:
                        energy_colour = GREEN
                    else:
                        energy_colour = RED
                    pygame.draw.line(screen, energy_colour, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.left + each.rect.width* energy_remain , each.rect.top - 5), 2)


                    #播放大飞机飞行音效
                    if each.rect.bottom == 0:
                        enemy3_fly_sound.play()

                else:     #大飞机毁灭

                    if not(delay % 3):
                        if e3_destroy_index == 0:
                            enemy3_die_sound.play()
                        screen.blit(each.destroy_images[e3_destroy_index], each.rect)
                        e3_destroy_index = (e3_destroy_index + 1) % 7
                        if e3_destroy_index == 0:
                            score += 100
                            each.reset()
                            enemy3_fly_sound.stop()


            # 绘制中型敌机
            for each in mid_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image, each.rect)

                    # 中飞机血槽
                    pygame.draw.line(screen, BLACK, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.right, each.rect.top - 5), \
                                     2)
                    # 生命大于30%显示绿色血条，否则为红色
                    energy_remain = each.energy / enemy.MidEnemy.energy
                    if energy_remain > 0.2:
                        energy_colour = GREEN
                    else:
                        energy_colour = RED
                    pygame.draw.line(screen, energy_colour, \
                                     (each.rect.left, each.rect.top - 5), \
                                     (each.rect.left + each.rect.width * energy_remain, \
                                     each.rect.top - 5), 2)


                else:   #毁灭
                    if not(delay % 3):
                        if e2_destroy_index == 0:
                            enemy2_die_sound.play()
                        screen.blit(each.destroy_images[e2_destroy_index], each.rect)
                        e2_destroy_index = (e2_destroy_index + 1) % 5
                        if e2_destroy_index == 0:
                            score += 60
                            each.reset()

            # 绘制小型敌机
            for each in small_enemies:
                if each.active:
                    each.move()
                    screen.blit(each.image, each.rect)

                else:   #毁灭
                    if e1_destroy_index == 0:
                        enemy1_die_sound.play()
                    if not(delay % 3):
                        screen.blit(each.destroy_images[e1_destroy_index], each.rect)
                        e1_destroy_index = (e1_destroy_index + 1) % 4
                        if e1_destroy_index == 0:
                            score += 10
                            each.reset()

            #绘制补给包
            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image, bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply, me):
                    get_bomb_sound.play()
                    if bomb_num < 3:
                        bomb_num += 1
                    bomb_supply.active = False
            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image, bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply, me):
                    get_bomb_sound.play()
                    bullet_supply.active = False
                    #发射超级子弹
                    pygame.time.set_timer(DOUBLE_TIME, 20*1000)
                    is_double_bullet = True

            if not lnvincible_mode:
                #检测我方飞机是否被撞
                enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
                if enemies_down:
                    for e in enemies_down:
                        if e.active:
                            me.active = False
                            bomb_num = 3
                            e.active = False
                            is_double_bullet = False


            if myplane_num > 0:
                for i in range(myplane_num):
                    screen.blit(hero_image, (width - 10 - hero_rect.width * (i + 1), height - hero_rect.height - 10))
                # 绘制我方飞机
                if not lnvincible_mode:
                    if not (delay % 5):  # 切换图片
                        switch_image = not switch_image
                    if me.active:
                        if switch_image:
                            screen.blit(me.image1, me.rect)
                        else:
                            screen.blit(me.image2, me.rect)
                    else:   #毁灭
                        if not (delay % 3):
                            screen.blit(me.destroy_images[me_destroy_index], me.rect)
                            me_destroy_index = (me_destroy_index + 1) % 4
                            if me_destroy_index == 0:
                                myplane_num -= 1
                                me.reset()
                                lnvincible_mode = True
                                pygame.time.set_timer(USEREVENT+2, 4000)

                else:       #无敌状态下
                    if not (delay % 2):  # 切换图片
                        screen.blit(me.image1, me.rect)


        if myplane_num > 0:
            score_text = score_font.render("Score : %s" % str(score), True, RED)
            screen.blit(score_text, (10, 5))  # 分数显示
            screen.blit(pause_image, pause_rect)  # 显示暂停按钮

            bomb_text = score_font.render("X %d" % bomb_num, True, WHITE)  # 左下角显示炸弹剩余数量
            text_rect = bomb_text.get_rect()
            screen.blit(bomb_image, (10, height - 10 - bomb_rect.height))
            screen.blit(bomb_text, ((20 + text_rect.width), (height - text_rect.height - 10)))


        else:       #绘制结束游戏画面


            screen.blit(restart_image, restart_rect)
            screen.blit(gameover_image, gameover_rect)
            pygame.mixer.music.stop()
            pygame.mixer.stop()
            pygame.time.set_timer(SUPPLY_TIME, 0)
            if not recorded:
                #读取历史最高得分
                recorded = True
                with open("record.txt", "r") as f:
                    record_score = int(f.read())
                if score > record_score:
                    with open("record.txt", "w") as f:
                        f.write(str(score))
            # 分数显示
            yourscore_text = score_font.render("Your Score : %s" % str(score), True, RED)
            screen.blit(yourscore_text, (80, 200))
            record_score_text = score_font.render("Best Score : %s" % record_score, True, RED)
            screen.blit(record_score_text, (80, 260))

        pygame.display.flip()
        delay -= 1
        if not delay:
            delay = 100
        clock.tick(50)

if __name__ == "__main__":
    main()


