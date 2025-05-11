import pygame
import random
import time

# กำหนดขนาดหน้าต่าง
WIDTH, HEIGHT = 800, 600
FPS = 60

# กำหนดสี
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# กำหนดการตั้งค่าของเกม
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Yakiniku Game")
clock = pygame.time.Clock()

# สร้างตัวแปรที่ใช้ในเกม
grill_rect = pygame.Rect(200, 150, 400, 300)  # กระทะ
meat_rect = pygame.Rect(random.randint(250, 550), random.randint(200, 400), 50, 50)  # เนื้อ

meat_speed = 5
grill_hotspot = pygame.Rect(400, 300, 10, 10)  # จุดที่ร้อนที่สุดในกระทะ
meat_burned = False

font = pygame.font.Font(None, 36)

# ฟังก์ชันแสดงข้อความ
def display_message(message, color, y_offset=0):
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(text, text_rect)

# ฟังก์ชันเกมหลัก
def game_loop():
    global meat_rect, meat_burned
    score = 0
    start_time = time.time()

    while True:
        screen.fill(WHITE)
        # print(pygame.time.Clock().get_time())
        # print(clock)
        # ตรวจสอบเหตุการณ์
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # ควบคุมการย้ายเนื้อ
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and meat_rect.left > grill_rect.left:
            meat_rect.x -= meat_speed
        if keys[pygame.K_RIGHT] and meat_rect.right < grill_rect.right:
            meat_rect.x += meat_speed
        if keys[pygame.K_UP] and meat_rect.top > grill_rect.top:
            meat_rect.y -= meat_speed
        if keys[pygame.K_DOWN] and meat_rect.bottom < grill_rect.bottom:
            meat_rect.y += meat_speed

        # ตรวจสอบว่าเนื้อไหม้ไหม
        if meat_rect.colliderect(grill_hotspot):
            meat_burned = True

        # วาดกระทะและเนื้อ
        pygame.draw.rect(screen, BLACK, grill_rect, 2)
        pygame.draw.rect(screen, GREEN, meat_rect)
        pygame.draw.rect(screen, RED, grill_hotspot)

        # แสดงคะแนนและสถานะ
        display_message(f"Score: {score}", BLACK, -200)
        if meat_burned:
            display_message("Game Over! Meat Burned!", RED, 0)
            break
        else:
            print(time.time(),start_time,time.time() - start_time)

            elapsed_time = time.time() - start_time
            display_message(f"Time: {int(elapsed_time)}s", BLACK, 200)

        pygame.display.flip()
        clock.tick(FPS)

        score = int(elapsed_time)  # คะแนนจะขึ้นตามเวลาที่ผ่านไป

# เริ่มเกม    
game_loop()
pygame.quit()