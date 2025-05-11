import pygame
pygame.init()
import random
def clamp(value, min_value=0, max_value=255):
    return max(min_value, min(value, max_value))
class cow:
    def __init__(self,x,y):
        self.rect = pygame.Rect(x, y, 50, 100)
        self.grade = 10
        self.badtick = 0
        self.active = True
        self.time = pygame.time.get_ticks()
        self.color = (0,255,255)
        self.canrnd = True
        self.trigger = False
        self.tmp_time  = 0
        self.cooldonw = 0 
        self.rand = random.randrange(1,7)
    def update(self):
        if self.trigger == False and ((pygame.time.get_ticks() - self.cooldonw)/1000 >= 1) :
            self.color = (0,255,255)
        if( pygame.time.get_ticks() - self.time)/1000 >= 10  :
            if self.trigger:
                self.grade -= (pygame.time.get_ticks() - self.tmp_time)/1000
            self.active = False
        if self.active and self.canrnd and ((pygame.time.get_ticks() - self.cooldonw)/1000 >= self.rand):
            # # if random.randrange(0,10) > 7 :
            #     print('onrand')
                
                self.canrnd = False
                self.color = (255,0,0)
                self.tmp_time = pygame.time.get_ticks()
                self.trigger = True
        
    def pet(self,x):

        if self.trigger :
            if self.rect.collidepoint(x) :
                print('fix')
                self.grade -= (pygame.time.get_ticks() - self.tmp_time)/1000
                self.color = (0,255,0)
                self.canrnd = True
                self.trigger = False
                self.cooldonw = pygame.time.get_ticks()
                self.rand = random.randrange(1,7)
    def __del__(self):
        del self

class customer:
    def __init__(self):
        self.order = None
    def generate_order(self,menu):
        import random
        return random.choice(menu)

class meat:
    def __init__(self,x,y,grade,color):
        self.rect = pygame.Rect(x,y,50,50)
        self.grade = grade 
        self.color = color
        self.base_color = color
        self.show = False
        self.cooking = False
        self.cooked = 0
        self.max_cooked = 10
        self.permcook = True
    # def cook(self,time) :
    #     if self.cooking:
    #         self.cooked -= time/1000
    #         print('cooking')
    #         progress = 1 - (self.cooked / self.max_cooked)
    #         r = (int(self.base_color[0] * (1 - progress)))
    #         g = (int(self.base_color[1] * (1 - progress)))
    #         b = (int(self.base_color[2] * (1 - progress)))
    #         self.color = tuple((r, g, b))
    # def cook(self, delta_time):
    #     if self.cooking:
    #         self.cooked += delta_time / 1000  # เพิ่มเวลาที่ปิ้ง (วินาที)
    #         print('cooking', self.cooked)

    #         # จำกัดไม่ให้เกิน max_cooked
    #         if self.cooked > self.max_cooked:
    #             self.cooked = self.max_cooked

    #         # เปลี่ยนสีให้ดูเหมือนไหม้ (ดำขึ้นเรื่อย ๆ)
    #         progress = self.cooked / self.max_cooked  # จาก 0 → 1
    #         r = int(self.base_color[0] * (1 - progress))
    #         g = int(self.base_color[1] * (1 - progress))
    #         b = int(self.base_color[2] * (1 - progress))

            # self.color = (r, g, b)
    def cook(self, screen, delta_time):
        if self.cooking and self.permcook:
            self.cooked += delta_time / 1000
            self.cooked = min(self.cooked, self.max_cooked)

            progress = self.cooked / self.max_cooked
            r = int(self.base_color[0] * (1 - progress))
            g = int(self.base_color[1] * (1 - progress))
            b = int(self.base_color[2] * (1 - progress))
            self.color = (r, g, b)

            # --- draw progress bar ---
            bar_width = 50
            bar_height = 8
            bar_x = self.rect.x
            bar_y = self.rect.y - 12

            fill_width = int(bar_width * progress)
            bar_color = (int(255 * progress), int(255 * (1 - progress)), 0)

            pygame.draw.rect(screen, (40, 40, 40), (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(screen, bar_color, (bar_x, bar_y, fill_width, bar_height))
class game:
    def __init__(self):
        self.buy = pygame.Rect(0, 150, 50, 100)
        self.farm = []
        self.meat = []
        self.score = 0
        self.click = 0
        self.time = 0
        self.posx = 0
        self.posy = 0

        pass
    def play(self):
        order = []
        pygame.init()
        screen = pygame.display.set_mode((900,800))
        WHITE = (255, 255, 255)
        is_running  = True
        font = pygame.font.SysFont('Arial', 36)
        RED = (255, 0, 0)
        Blue = (0,255,0)
        a = pygame.time.get_ticks()
        box = pygame.Rect(100,150,50,50)
        mx  = 50
        my = 50
        drag = None
        pan_color = (0, 200, 255)
        pan_pos = (300, 200)
        rice = pygame.Rect(400,200,200,200)
        
        pan_radius = 50
        clock = pygame.time.Clock()
        while is_running :
            delta_time = clock.tick(60)
            screen.fill(WHITE)
            pygame.draw.rect(screen,(255,0,0),self.buy)
            pygame.draw.rect(screen,(255,0,0),box)
            pygame.draw.circle(screen, pan_color, pan_pos, pan_radius)
            pygame.draw.rect(screen,(223,25,21),rice)
            
            # pygame.draw.rect(screen,(255,0,0),self.buy)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.buy.collidepoint(event.pos):
                        print('addcow')
                        self.farm.append(cow(self.posx,self.posy))
                        self.posx += 100
                        # self.posy += 100
                    if box.collidepoint(event.pos):
                        for i in self.meat :
                            if i.show == False :
                                i.show = True 
                                break
                    if event.button == 1:
                        for i,j  in enumerate(self.meat) :
                            if j.rect.collidepoint(event.pos) and j.show == True:
                                drag = i
                
                    for u in self.farm:
                        u.pet(event.pos)
                if event.type == pygame.MOUSEBUTTONUP:
                    import math
                    if event.button == 1 :
                        if drag != None :
                            mouse_pos = event.pos
                            distance = math.hypot(mouse_pos[0] - pan_pos[0], mouse_pos[1] - pan_pos[1])
                            if distance <= pan_radius:
                                # self.meat[drag].color = (24,44,232)
                                self.meat[drag].cooking = True
                            else:
                                # self.meat[drag].color = (233,42,11)
                                self.meat[drag].cooking = False
                            if rice.collidepoint(mouse_pos) :
                                self.meat[drag].permcook = False
                                self.meat[drag].color = (255,0,0)
                            drag = None
                            
                if event.type == pygame.MOUSEMOTION:
                    if drag != None :
                        self.meat[drag].rect.move_ip(event.rel)
                # print(self.farm)
                    
            for i in self.farm :
                i.update()
                if i.active :                        
                    pygame.draw.rect(screen, i.color, i.rect)
                else:
                    if i.grade > 8 :
                        color = (0,255,0)
                    elif 5 <= i.grade < 8 :
                        color = (255,0,0)
                    else :
                        color = (0,0,0)
                    self.meat.append(meat(mx,my,i.grade,color))
                    self.farm.remove(i)
                    mx += 20
    
                    del i
            for i in self.meat:
                if i.show == True :
                    print(i.color)
                    pygame.draw.rect(screen,i.color,i.rect)
                    i.cook(screen, delta_time)
            # print(self.farm)
            # print(self.meat)
            
            
            text = font.render(f'{(pygame.time.get_ticks() - a ) / 1000:.0f}', True, Blue)
            screen.blit(text, (200, 200))
            pygame.display.flip()
if __name__ == '__main__' :

    pygame.init()

    a = game()
    a.play()

