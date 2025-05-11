import pygame
import random
pygame.init()
# class cow:

    # def __init__(self):
    #     self.meatgrade = ''
    #     self.time = time.time()
    # def pet(self):
    #     if self.time - time.time() == 10:
    #         self.del()
    #     else:
    #         if self.time - time.time() == 3:
    #             #ทำเสียง
    #             #เรียกให้กดที่ตัวเอง
hitbox = pygame.Rect(0, 150, 50, 100)
hitbox1 = pygame.Rect(100, 150, 100, 100)
hitbox2 = pygame.Rect(700, 150, 100, 100)
hitbox3 = pygame.Rect(500, 150, 100, 100)
hitbox4 = pygame.Rect(300, 250, 300, 100)
color = [(0,0,255),(255, 0, 0),(0,0,0),(0,255,0),(233,74,25)]
nig = []
nig.append(hitbox)
nig.append(hitbox1)
nig.append(hitbox2)
nig.append(hitbox3)
nig.append(hitbox4)
a = pygame.time.get_ticks()
screen = pygame.display.set_mode((900,800))
WHITE = (255, 255, 255)
RED = (255, 0, 0)
Blue = (0,255,0)
font = pygame.font.SysFont('Arial', 36)
while True:
    for event in pygame.event.get():
        # print(a)
        # print(pygame.time.get_ticks())
        # print((pygame.time.get_ticks() - a ) / 1000)
        
        # if (pygame.time.get_ticks() - a ) / 1000 >= 10:
        #     quit()
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # ตรวจสอบว่าคลิกใน hitbox หรือไม่
            for i in nig:
                
                if i.collidepoint(event.pos):  # event.pos คือพิกัดของเมาส์ที่คลิก
                    print(f"คลิกใน hitbox!{i}")
                    # tmp = nig.index(i)
                    # nig.remove(i)
                    # color.remove(color[tmp])
                    a = random.randrange(0,255)
                    b = random.randrange(0,255)
                    c = random.randrange(0,255)
                    # color[nig.index(i)] = (a,b,c)
                    nig.append(pygame.Rect(random.randrange(0,100), random.randrange(0,100), random.randrange(0,100), random.randrange(0,100)))
                    color.append((a,b,c))
                    break
                
        if ((pygame.time.get_ticks() - a ) / 1000) >= 10 :

            screen.fill(WHITE)
            for i in nig:
                pygame.draw.rect(screen, color[nig.index(i)], i)
            
        else :
            screen.fill(WHITE)
            for i in nig:
                pygame.draw.rect(screen, color[nig.index(i)], i)
        
        
        text = font.render(f'{(pygame.time.get_ticks() - a ) / 1000:.0f}', True, Blue)
        screen.blit(text, (200, 200))
        pygame.display.flip()