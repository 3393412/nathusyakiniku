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
    def __init__(self,wait):
        self.order = None
        self.order_time = pygame.time.get_ticks()
        self.wait_limit = wait # 8 วิ
        self.font = pygame.font.SysFont('Arial', 24)
        self.correct = False
        self.customerscore = 0
        self.slow  = False
    def generate_order(self, menu):
        import random
        self.order = random.choice(menu)
        self.order_time = pygame.time.get_ticks()
        print(f'New order:{self.order}')

    def update(self,score):
        now = pygame.time.get_ticks()
        if now - self.order_time > self.wait_limit:
            # print('ไปละ')
            self.order = None
            self.slow = True
            # print(score)
            # score -= 1000
            # print(score)

    def check_delivery(self, serve):
        if self.order is not None and serve == self.order:
            print("✅ Correct meat delivered!")
            self.order = None
            now = pygame.time.get_ticks()
            using_time = now - self.order_time /1000
            if  using_time< 20 :
                self.customerscore += 20
            elif 20 < using_time <= 40 :
                self.customerscore += 15
            self.customerscore += 20
            return True
        else :
            return False
    def draw(self, screen,text):
        if self.order is not None:
            # เวลาเหลือ
            time_left = max(0, (self.wait_limit - (pygame.time.get_ticks() - self.order_time)) // 1000)

            # ข้อความแสดงคำสั่ง
            order_text = self.font.render(f"Order:{self.order}", True, (0, 0, 0))
            time_text = self.font.render(f"Time left: {time_left}s", True, (255, 0, 0))

            # แสดงที่มุมซ้ายบน
            tmp = (text[0],text[1]+30)
            screen.blit(order_text, dest = text)
            screen.blit(time_text, dest = tmp)

class meat:
    def __init__(self,x,y,grade,color):
        if grade < 5 :
            image = pygame.image.load("projek/meat_rott.png").convert_alpha()
        elif 5 <= grade < 8 :
            image = pygame.image.load("projek/meat.png").convert_alpha()
        else : 
            image = pygame.image.load("projek/neat_aura.png").convert_alpha()
        self.rect = image.get_rect(topleft=(x, y))
        self.image = image
        self.grade = grade 
        self.color = color
        self.base_color = color
        self.show = False
        self.cooking = False
        self.cooked = 0
        self.max_cooked = 10
        self.permcook = True
        self.menu = None
    def cook(self, screen, delta_time):
        if self.cooking and self.permcook:
            self.cooked += delta_time / 1000
            self.cooked = min(self.cooked, self.max_cooked)

            progress = self.cooked / self.max_cooked
            if 3<= self.cooked <= 5 :
                tmp = pygame.image.load("projek/meatcooking.png").convert_alpha()
                self.image = tmp
                self.menu = 'Medium-rare'
            elif 6 <= self.cooked < 8 :
                tmp = pygame.image.load("projek/meat-cooked.png").convert_alpha()
                self.image = tmp
                self.menu = 'Cooked'
            elif self.cooked >= 8 :
                tmp = pygame.image.load("projek/meat_dead.png").convert_alpha()
                self.image = tmp
                self.menu = 'Toasted'
            bar_width = 100
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
        self.click = 0
        self.time = 0
        self.posx = 0
        self.posy = 0
        self.score = 5000
        self.money = 100000000
        self.game_time = 90
        self.total_click = 0
        self.total_time = self.game_time
        self.total_cooked = 0
        self.total_score = 0
        self.total_serve = 0
        self.mouse_data = []
        self.is_menu = True
        self.is_game = True
        self.is_running = True
        self.is_help = True
        self.screen = pygame.display.set_mode((900,800))
        pass
    # def program(self) :

    def help(self):
        self.screen.fill((255,255,255))
        background = pygame.image.load("projek/คินนิคุแมน_Website_1200x628.jpg").convert()
        self.screen.blit(background, (0, 0))
        backgui = pygame.Rect(200,200,300,75)

        while self.is_help :
            self.screen.blit(background, (0, 0))
            pygame.draw.rect(self.screen,(0,212,255),backgui)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_help = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if backgui.collidepoint(event.pos) :
                        self.is_help = False
                        self.is_menu = True
                        self.menu()
                    # if help.collidepoint(event.pos) :
                    #     self.is_menu = False
                    #     self.help()
            pygame.display.flip()
    def menu(self):
        self.screen.fill((255,255,255))
        background = pygame.image.load("projek/01kinniku-00a.jpg").convert()

        helpx = 450 - 125
        helpy= 520
        playx = 450 - 175 
        playy = 400
        datax = 450 - 100
        datay = helpy + 100
        settingx = 10
        settingy = 740
        setting = pygame.Rect(settingx,settingy,50,50)
        help = pygame.Rect(helpx,helpy,250,70)
        playgui = pygame.Rect(playx,playy,350,100)
        data = pygame.Rect(datax,datay,200,70)
        while self.is_menu :
            self.screen.blit(background, (0, 0))
            pygame.draw.rect(self.screen,(0,255,0),setting)
            pygame.draw.rect(self.screen,(0,212,255),data)
            pygame.draw.rect(self.screen,(0,212,255),help)
            pygame.draw.rect(self.screen,(0,212,255),playgui)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_menu = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if playgui.collidepoint(event.pos) :
                        self.is_menu = False
                        self.play()
                    if help.collidepoint(event.pos) :
                        self.is_menu = False
                        self.is_help = True
                        self.help()
            pygame.display.flip()
    def play(self):
        self.screen.fill((255,255,255))
        cowslot = 3
        currentcow = 1
        order = []
        menu = ['Cooked-Meat-Rice','Cooked-Steak','Medium-rare-Rice','Medium-rare-Steak','Soiju']
        pygame.init()
        # screen = pygame.display.set_mode((900,800))
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
        ricex = 400
        ricey = 200
        rice = pygame.Rect(ricex,ricey,200,200)
        rice_image = pygame.image.load("projek/rice.png").convert_alpha()
        steakx = 600
        steaky = 200
        steak = pygame.Rect(steakx,steaky,200,200)
        soijux = 600
        soijuy = 400
        soiju = pygame.Rect(soijux,soijuy,200,200)
        pan_radius = 50
        clock = pygame.time.Clock()
        serve = pygame.Rect(500,500,80,80)
        cowslotx = 100
        cowsloty = 300
        cowslotgui = pygame.Rect(cowslotx,cowsloty,50,50)
        trashx = 100
        trashy = 500
        trash = pygame.Rect(trashx,trashy,80,80)
        while self.is_game :
            delta_time = clock.tick(60)
            self.screen.fill(WHITE)
            pygame.draw.rect(self.screen,(0,212,255),trash)
            pygame.draw.rect(self.screen,(0,212,255),cowslotgui)
            pygame.draw.rect(self.screen,(0,0,255),soiju)
            pygame.draw.rect(self.screen,(0,0,255),steak)
            pygame.draw.rect(self.screen,(0,255,0),serve)
            pygame.draw.rect(self.screen,(255,0,0),self.buy)
            pygame.draw.rect(self.screen,(255,0,0),box)
            pygame.draw.circle(self.screen, pan_color, pan_pos, pan_radius)
            self.screen.blit(rice_image,(ricex,ricey))
            while len(order) < 5 :
                tmp2 = random.randrange(70,100)
                custom = customer(tmp2*1000)
                custom.generate_order(menu)
                order.append(custom)
            # p = order.copy()
            for i in order :
                if i.order == None :
                    if i.slow == True :
                        self.score -= 0
                    order.remove(i)
                    break
                i.update(self.score)
            for i in range(len(order)):
                x = 500 
                y = 50
                dest = (x - (i * 300),y)
                # print(type(dest))
                order[i].draw(self.screen,dest)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.total_click += 1
                    if self.buy.collidepoint(event.pos) and (currentcow <= cowslot) and self.money >= 15:
                        self.money -= 15
                        
                        
                        print('addcow')
                        self.posx = 100 * ((currentcow-1))
                        currentcow += 1
                        self.farm.append(cow(self.posx,self.posy))
                        

                    if box.collidepoint(event.pos):
                        for i in self.meat :
                            if i.show == False :
                                i.show = True 
                                break
                    if event.button == 1:
                        for i,j  in enumerate(self.meat) :
                            if j.rect.collidepoint(event.pos) and j.show == True:
                                drag = i
                    if cowslotgui.collidepoint(event.pos) and cowslot <= 8 :
                            if self.money >= 85 :
                                self.money -= 85 
                                cowslot += 1
                    for u in self.farm:
                        u.pet(event.pos)
                if event.type == pygame.MOUSEBUTTONUP:
                    import math
                    if event.button == 1 :
                        if drag != None :
                            mouse_pos = event.pos
                            distance = math.hypot(mouse_pos[0] - pan_pos[0], mouse_pos[1] - pan_pos[1])
                            if distance <= pan_radius:
                                
                                self.meat[drag].cooking = True
                            else:
   
                                self.meat[drag].cooking = False
                            if rice.collidepoint(mouse_pos)and self.meat[drag].menu != None:
                                self.meat[drag].permcook = False
                                self.meat[drag].color = (255,0,0)
                                self.meat[drag].image = pygame.image.load("projek/plate_kat_med.png").convert_alpha()
                                if self.meat[drag].menu == 'Cooked' :
                                    self.meat[drag].menu += '-Meat-Rice'
                                    self.total_cooked += 1 
                                else :
                                    self.meat[drag].menu += '-Rice'
                                    self.total_cooked += 1
                            if trash.collidepoint(mouse_pos) :
                                self.meat.remove(self.meat[drag]) 
                            if steak.collidepoint(mouse_pos)and self.meat[drag].menu != None :
                                self.meat[drag].permcook = False
                                self.meat[drag].menu += '-Steak'
                                self.total_cooked += 1
                            if soiju.collidepoint(mouse_pos) and self.meat[drag].menu == None :
                                self.meat[drag].permcook = False
                                self.meat[drag].menu = 'Soiju'
                                self.total_cooked += 1
                            if serve.collidepoint(mouse_pos) and self.meat[drag].menu != None :
                                for i in order :
                                    
                                    crr = i.check_delivery(self.meat[drag].menu)
                                    if crr :
                                        
                                        # print(i.customerscore)
                                        # print(i.customerscore * (1+(0.1 *(self.meat[drag].grade))))
                                        self.score += i.customerscore * (1+(0.1 *(self.meat[drag].grade)))
                                        self.meat.remove(self.meat[drag])

                                        self.game_time += 15
                                        self.total_time += 15
                                        break
                                    else : 
                                        self.score -= 30
                                        self.game_time -= 10
                                        self.meat.remove(self.meat[drag])
                                        break
                                self.total_serve += 1
                                self.total_score += self.score
                                        

                                        
                            drag = None
                            
                if event.type == pygame.MOUSEMOTION:
                    if drag != None :
                        self.meat[drag].rect.move_ip(event.rel)
                    self.mouse_data.append({"time": pygame.time.get_ticks(),
            "pos": event.pos,
            "rel": event.rel,
        })
                    
            for i in self.farm :
                i.update()
                if i.active :                        
                    pygame.draw.rect(self.screen, i.color, i.rect)
                else:
                    currentcow -= 1
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
                    # pygame.draw.rect(screen,i.color,i.rect,0)
                    self.screen.blit(i.image,(i.rect.x,i.rect.y))
                    i.cook(self.screen, delta_time)

            click = font.render(f'{self.total_click}', True, Blue)
            text = font.render(f'{self.game_time-(pygame.time.get_ticks() / 1000):.0f}', True, Blue)
            score = font.render(f'{self.score}', True, Blue)
            money = font.render(f'{self.money}', True, Blue)
            self.screen.blit(text, (200, 200))
            self.screen.blit(score, (200, 400))
            self.screen.blit(money, (200, 300))
            self.screen.blit(click, (200, 500))
            pygame.display.flip()
if __name__ == '__main__' :

    pygame.init()
    
    a = game()
    a.menu()
    # a.play()

