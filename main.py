#python 小游戏

import pygame
import sys
import random
import math

# 导入游戏模块
from game.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, BLACK, RED, GREEN, BLUE, ORANGE, DARK_RED, GOLD
from game.entities.player import Player
from game.entities.enemy import Enemy
from game.entities.bullet import Bullet
from game.entities.gold import Gold
from game.entities.effect import Effect
from game.items.weapon import weapons
from game.items.shop import shop_items

# 初始化Pygame
pygame.init()
pygame.mixer.init()

# 创建游戏窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brotato-like Game")

# 游戏时钟
clock = pygame.time.Clock()

# 游戏状态
GAME_STATE = "playing"  # playing, shop, game_over

# 波次系统
wave = 1
wave_enemies = 0
wave_enemies_total = 10
wave_timer = 0
wave_duration = 30000  # 30秒

# 初始化游戏对象
player = Player()
enemies = []
bullets = []
gold = []
effects = []

# 敌人生成计时器
enemy_spawn_timer = 0
enemy_spawn_interval = 1000  # 毫秒

# 射击计时器
shoot_timer = 0

# 游戏主循环
running = True
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # 获取键盘输入
    keys = pygame.key.get_pressed()
    
    # 更新游戏状态
    if GAME_STATE == "playing":
        # 移动玩家
        player.move([keys[pygame.K_w], keys[pygame.K_s], keys[pygame.K_a], keys[pygame.K_d]], SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # 生成敌人
        current_time = pygame.time.get_ticks()
        if current_time - enemy_spawn_timer > enemy_spawn_interval and wave_enemies < wave_enemies_total:
            # 从屏幕边缘生成敌人
            side = random.randint(0, 3)
            if side == 0:  # 顶部
                x = random.randint(0, SCREEN_WIDTH)
                y = -20
            elif side == 1:  # 右侧
                x = SCREEN_WIDTH + 20
                y = random.randint(0, SCREEN_HEIGHT)
            elif side == 2:  # 底部
                x = random.randint(0, SCREEN_WIDTH)
                y = SCREEN_HEIGHT + 20
            else:  # 左侧
                x = -20
                y = random.randint(0, SCREEN_HEIGHT)
            
            # 随机选择敌人类型，随着波次增加，高级敌人出现概率增加
            enemy_types = ["basic", "fast", "tank"]
            weights = [max(0.5, 0.7 - wave * 0.05), min(0.3, 0.2 + wave * 0.03), min(0.2, 0.1 + wave * 0.02)]
            enemy_type = random.choices(enemy_types, weights=weights)[0]
            
            # 根据敌人类型选择颜色
            if enemy_type == "basic":
                color = RED
            elif enemy_type == "fast":
                color = ORANGE
            elif enemy_type == "tank":
                color = DARK_RED
            
            enemies.append(Enemy(x, y, enemy_type, color))
            wave_enemies += 1
            enemy_spawn_timer = current_time
        
        # 射击
        shoot_interval = 1000 / player.weapon.attack_speed
        if current_time - shoot_timer > shoot_interval:
            # 向鼠标方向射击
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dx = mouse_x - player.x
            dy = mouse_y - player.y
            distance = (dx**2 + dy**2)**0.5
            if distance > 0:
                dx /= distance
                dy /= distance
                
                # 根据武器的子弹数量射击
                if player.weapon.bullet_count == 1:
                    # 单子弹
                    bullets.append(Bullet(player.x, player.y, dx, dy, player.weapon.damage, player.weapon.range))
                elif player.weapon.bullet_count > 1:
                    # 多子弹，分散射击
                    angle_step = 0.3 / (player.weapon.bullet_count - 1)
                    for i in range(player.weapon.bullet_count):
                        angle = -0.15 + i * angle_step
                        new_dx = dx * math.cos(angle) - dy * math.sin(angle)
                        new_dy = dx * math.sin(angle) + dy * math.cos(angle)
                        bullets.append(Bullet(player.x, player.y, new_dx, new_dy, player.weapon.damage, player.weapon.range))
            shoot_timer = current_time
        
        # 更新敌人
        for enemy in enemies[:]:
            enemy.move(player)
            # 检查敌人是否与玩家碰撞
            dx = enemy.x - player.x
            dy = enemy.y - player.y
            distance = (dx**2 + dy**2)**0.5
            if distance < (player.width + enemy.width) // 2:
                player.health -= enemy.damage
                enemies.remove(enemy)
                if player.health <= 0:
                    GAME_STATE = "game_over"
        
        # 更新子弹
        for bullet in bullets[:]:
            if not bullet.update():
                bullets.remove(bullet)
            else:
                # 检查子弹是否击中敌人
                for enemy in enemies[:]:
                    dx = bullet.x - enemy.x
                    dy = bullet.y - enemy.y
                    distance = (dx**2 + dy**2)**0.5
                    if distance < (enemy.width // 2):
                        enemy.health -= bullet.damage
                        # 添加击中特效
                        effects.append(Effect(enemy.x, enemy.y, "hit"))
                        bullets.remove(bullet)
                        if enemy.health <= 0:
                            # 敌人死亡，掉落金币
                            if random.random() < 0.7:  # 70%概率掉落金币
                                gold_amount = random.randint(10, 30)
                                gold.append(Gold(enemy.x, enemy.y, gold_amount))
                            # 添加爆炸特效
                            effects.append(Effect(enemy.x, enemy.y, "explosion"))
                            enemies.remove(enemy)
                        break
        
        # 更新金币
        for gold_piece in gold[:]:
            if gold_piece.collect(player):
                gold.remove(gold_piece)
        
        # 更新特效
        for effect in effects[:]:
            if not effect.update():
                effects.remove(effect)
        
        # 检查波次是否结束
        if len(enemies) == 0 and wave_enemies >= wave_enemies_total:
            # 波次结束，进入商店阶段
            GAME_STATE = "shop"
    
    elif GAME_STATE == "shop":
        # 商店逻辑
        if keys[pygame.K_SPACE]:
            # 开始下一波
            wave += 1
            wave_enemies = 0
            wave_enemies_total = 10 + wave * 5  # 每波增加5个敌人
            enemy_spawn_interval = max(500, 1000 - wave * 50)  # 每波减少生成间隔
            GAME_STATE = "playing"
        
        # 处理商店购买
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        
        for i, item in enumerate(shop_items):
            item_x = SCREEN_WIDTH // 2 - 150
            item_y = 150 + i * 60
            
            # 检查鼠标是否悬停在物品上
            if item_x <= mouse_pos[0] <= item_x + 300 and item_y <= mouse_pos[1] <= item_y + 40:
                if mouse_clicked:
                    # 检查是否有足够的金币
                    if player.gold >= item["price"]:
                        # 购买物品
                        player.gold -= item["price"]
                        
                        # 应用物品效果
                        if item["effect"] == "health":
                            player.health = min(player.max_health, player.health + item["value"])
                        elif item["effect"] == "speed":
                            player.speed += item["value"]
                        elif item["effect"] == "attack_speed":
                            player.attack_speed += item["value"]
                        elif item["effect"] == "damage":
                            player.weapon.damage += item["value"]
                        elif item["effect"] == "weapon":
                            player.weapon = weapons[item["value"]]
    
    # 绘制游戏
    screen.fill(BLACK)
    
    if GAME_STATE == "playing":
        # 绘制玩家
        player.draw(screen, GREEN)
        
        # 绘制敌人
        for enemy in enemies:
            enemy.draw(screen)
        
        # 绘制子弹
        for bullet in bullets:
            bullet.draw(screen, BLUE)
        
        # 绘制金币
        for gold_piece in gold:
            gold_piece.draw(screen, GOLD)
        
        # 绘制特效
        for effect in effects:
            if effect.effect_type == "explosion":
                effect.draw(screen, ORANGE)
            elif effect.effect_type == "hit":
                effect.draw(screen, RED)
        
        # 绘制玩家信息
        font = pygame.font.Font(None, 36)
        health_text = font.render(f"Health: {player.health}", True, WHITE)
        screen.blit(health_text, (10, 10))
        
        # 绘制金币信息
        gold_text = font.render(f"Gold: {player.gold}", True, GOLD)
        screen.blit(gold_text, (10, 50))
        
        # 绘制波次信息
        wave_text = font.render(f"Wave: {wave}", True, WHITE)
        screen.blit(wave_text, (10, 90))
        enemies_text = font.render(f"Enemies: {wave_enemies_total - wave_enemies}", True, WHITE)
        screen.blit(enemies_text, (10, 130))
    
    elif GAME_STATE == "shop":
        # 绘制商店界面
        font = pygame.font.Font(None, 48)
        shop_text = font.render("Shop", True, WHITE)
        screen.blit(shop_text, (SCREEN_WIDTH//2 - 50, 50))
        
        # 绘制金币信息
        font = pygame.font.Font(None, 36)
        gold_text = font.render(f"Gold: {player.gold}", True, GOLD)
        screen.blit(gold_text, (10, 10))
        
        # 绘制商店物品
        mouse_pos = pygame.mouse.get_pos()
        for i, item in enumerate(shop_items):
            item_x = SCREEN_WIDTH // 2 - 150
            item_y = 150 + i * 60
            
            # 检查鼠标是否悬停在物品上
            if item_x <= mouse_pos[0] <= item_x + 300 and item_y <= mouse_pos[1] <= item_y + 40:
                # 绘制高亮背景
                pygame.draw.rect(screen, (50, 50, 50), (item_x, item_y, 300, 40))
            
            # 绘制物品名称和价格
            item_text = font.render(f"{item['name']} - ${item['price']}", True, WHITE)
            screen.blit(item_text, (item_x + 10, item_y + 5))
        
        # 绘制继续按钮
        continue_text = font.render("Press SPACE to start next wave", True, WHITE)
        screen.blit(continue_text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT - 100))
    
    # 绘制游戏状态
    if GAME_STATE == "game_over":
        font = pygame.font.Font(None, 48)
        game_over_text = font.render("Game Over", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - 70, SCREEN_HEIGHT//2))
    
    # 更新显示
    pygame.display.flip()
    
    # 控制帧率
    clock.tick(FPS)

# 退出游戏
pygame.quit()
sys.exit()
