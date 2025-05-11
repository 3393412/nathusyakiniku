import pygame
import random
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
        if( pygame.time.get_ticks() - self.time)/1000 >= 3  :
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
    def generate_order(self, menu):
        import random
        self.order = random.choice(menu)
        self.order_time = pygame.time.get_ticks()
        print(f'New order:{self.order}')

    def update(self, menu):
        now = pygame.time.get_ticks()
        if now - self.order_time > self.wait_limit:
            self.order = None

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
        image = pygame.image.load("projek/meat.png").convert_alpha()
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

class Screen:
    def __init__(self, screen):
        self.screen = screen

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self):
        pass

class GameScreen(Screen):
    def __init__(self, screen,prog):
        super().__init__(screen)
        self.prog = prog
        self.buy = pygame.Rect(0, 150, 50, 100)
        self.farm = []
        self.meat = []
        self.score = 0
        self.click = 0
        self.time = 0
        self.posx = 0
        self.posy = 0
        self.score = 0 
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
        self.screen = screen
        self.order = []
        self.cowslot = 3
        self.currentcow = 1
        self.drag = None
    def play(self):
        
        menu = ['Cooked-Meat-Rice','Cooked-Steak','Medium-rare-Rice','Medium-rare-Steak','Soiju']
        WHITE = (255, 255, 255)
        font = pygame.font.SysFont('Arial', 36)
        RED = (255, 0, 0)
        Blue = (0,255,0)
        a = pygame.time.get_ticks()
        self.box = pygame.Rect(100,150,50,50)
        mx  = 50
        my = 50
        drag = None
        pan_color = (0, 200, 255)
        self.pan_pos = (300, 200)
        ricex = 400
        ricey = 200
        self.rice = pygame.Rect(ricex,ricey,200,200)
        rice_image = pygame.image.load("projek/rice.png").convert_alpha()
        steakx = 600
        steaky = 200
        self.steak = pygame.Rect(steakx,steaky,200,200)
        soijux = 600
        soijuy = 400
        self.soiju = pygame.Rect(soijux,soijuy,200,200)
        self.pan_radius = 50
        clock = pygame.time.Clock()
        self.serve = pygame.Rect(500,500,80,80)
        cowslotx = 100
        cowsloty = 300
        self.cowslotgui = pygame.Rect(cowslotx,cowsloty,50,50)
        delta_time = clock.tick(60)
        self.screen.fill(WHITE)
        pygame.draw.rect(self.screen,(0,212,255),self.cowslotgui)
        pygame.draw.rect(self.screen,(0,0,255),self.soiju)
        pygame.draw.rect(self.screen,(0,0,255),self.steak)
        pygame.draw.rect(self.screen,(0,255,0),self.serve)
        pygame.draw.rect(self.screen,(255,0,0),self.buy)
        pygame.draw.rect(self.screen,(255,0,0),self.box)
        pygame.draw.circle(self.screen, pan_color, self.pan_pos, self.pan_radius)
        self.screen.blit(rice_image,(ricex,ricey))
        while len(self.order) < 5 :
            tmp2 = random.randrange(70,100)
            custom = customer(tmp2*1000)
            custom.generate_order(menu)
            self.order.append(custom)
            # p = order.copy()
        for i in self.order :
            if i.order == None :
                self.order.remove(i)
            i.update(menu)
        for i in range(len(self.order)):
            x = 500 
            y = 50
            dest = (x - (i * 300),y)
            # print(type(dest))
            self.order[i].draw(self.screen,dest)

                    
        for i in self.farm :
            i.update()
            if i.active :                        
                pygame.draw.rect(self.screen, i.color, i.rect)
            else:
                self.currentcow -= 1
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
    def game_event(self,event):
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.total_click += 1
                if self.buy.collidepoint(event.pos) and (self.currentcow <= self.cowslot) and self.money >= 15:
                    self.money -= 15
                    self.currentcow += 1
                        
                    print('addcow')
                    self.posx = 100 * (self.currentcow-2)
                    self.farm.append(cow(self.posx,self.posy))
                        

                if self.box.collidepoint(event.pos):
                    for i in self.meat :
                        if i.show == False :
                            i.show = True 
                            break
                if event.button == 1:
                    for i,j  in enumerate(self.meat) :
                        if j.rect.collidepoint(event.pos) and j.show == True:
                            self.drag = i
                if self.cowslotgui.collidepoint(event.pos) and self.cowslot <= 8 :
                        if self.money >= 85 :
                            self.money -= 85 
                            self.cowslot += 1
                for u in self.farm:
                    u.pet(event.pos)
            if event.type == pygame.MOUSEBUTTONUP:
                import math
                if event.button == 1 :
                    if self.drag != None :
                        mouse_pos = event.pos
                        distance = math.hypot(mouse_pos[0] - self.pan_pos[0], mouse_pos[1] - self.pan_pos[1])
                        if distance <= self.pan_radius:
                                
                            self.meat[self.drag].cooking = True
                        else:
   
                            self.meat[self.drag].cooking = False
                        if self.rice.collidepoint(mouse_pos)and self.meat[self.drag].menu != None:
                            self.meat[self.drag].permcook = False
                            self.meat[self.drag].color = (255,0,0)
                            self.meat[self.drag].image = pygame.image.load("projek/plate_kat_med.png").convert_alpha()
                            if self.meat[self.drag].menu == 'Cooked' :
                                self.meat[self.drag].menu += '-Meat-Rice'
                                self.total_cooked += 1 
                            else :
                                self.meat[self.drag].menu += '-Rice'
                                self.total_cooked += 1 
                        if self.steak.collidepoint(mouse_pos)and self.meat[self.drag].menu != None :
                            self.meat[self.drag].permcook = False
                            self.meat[self.drag].menu += '-Steak'
                            self.total_cooked += 1
                        if self.soiju.collidepoint(mouse_pos) and self.meat[self.drag].menu == None :
                            self.meat[self.drag].permcook = False
                            self.meat[self.drag].menu = 'Soiju'
                            self.total_cooked += 1
                        if self.serve.collidepoint(mouse_pos) and self.meat[self.drag].menu != None :
                            for i in self.order :
                                    
                                crr = i.check_delivery(self.meat[self.drag].menu)
                                if crr :
                                        
                                    print(i.customerscore)
                                    print(i.customerscore * (1+(0.1 *(self.meat[self.drag].grade))))
                                    self.score = i.customerscore * (1+(0.1 *(self.meat[self.drag].grade)))
                                    self.meat.remove(self.meat[self.drag])
                      
                                    self.game_time += 15
                                    self.total_time += 15
                                    self.total_serve += 1
                                    self.total_score += self.score
                                    break

                                        
                        self.drag = None
                            
            if event.type == pygame.MOUSEMOTION:
                if self.drag != None :
                    self.meat[self.drag].rect.move_ip(event.rel)
                self.mouse_data.append({"time": pygame.time.get_ticks(),
        "pos": event.pos,
        "rel": event.rel,
    })
class MenuScreen(Screen):
    def __init__(self, screen,prog):
        super().__init__(screen)
        self.screen = screen
        self.prog = prog
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
        self.setting = pygame.Rect(settingx,settingy,50,50)
        self.help = pygame.Rect(helpx,helpy,250,70)
        self.playgui = pygame.Rect(playx,playy,350,100)
        self.data = pygame.Rect(datax,datay,200,70)
        self.screen.blit(background, (0, 0))
        pygame.draw.rect(self.screen,(0,255,0),self.setting)
        pygame.draw.rect(self.screen,(0,212,255),self.data)
        pygame.draw.rect(self.screen,(0,212,255),self.help)
        pygame.draw.rect(self.screen,(0,212,255),self.playgui)
    def menu_event(self,event,state) :
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.playgui.collidepoint(event.pos) :
                self.prog.state = 'play'
            if self.help.collidepoint(event.pos) :
                self.prog.state = 'help'

class Prog:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((900,800))
        self.clock = pygame.time.Clock()
        self.game = GameScreen(self.screen,self)
        self.menu = MenuScreen(self.screen,self)
        self.state = 'menu'
        self.running = True
    def run(self) :
        while self.running :
            # print(self.state)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if self.state == "menu":
                    self.menu.menu_event(event,self.state)
                elif self.state == "play":
                    self.game.game_event(event)
                elif self.state == "help":
                    self.handle_help_events(event)
            
            if self.state == "menu":
                self.menu.menu()
            elif self.state == 'play' :
                self.game.play()
            pygame.display.flip()
a =Prog()
a.run()