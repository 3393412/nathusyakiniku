import pygame
import random
import csv
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from stat_gui import StatViewer
def clamp(value, min_value=0, max_value=255):
    return max(min_value, min(value, max_value))

class cow:
    def __init__(self,x,y):
        self.rect = pygame.Rect(x, y, 100, 100)
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
        self.image = pygame.image.load("projek/cow.png")
        self.image = pygame.transform.scale(self.image,(100,100))
    def update(self):
        if self.trigger == False and ((pygame.time.get_ticks() - self.cooldonw)/1000 >= 1) :
            self.image = pygame.image.load("projek/cow.png")
            self.image = pygame.transform.scale(self.image,(100,100)) 
        if( pygame.time.get_ticks() - self.time)/1000 >= 10  :
            if self.trigger:
                self.grade -= (pygame.time.get_ticks() - self.tmp_time)/1000
            self.active = False
        if self.active and self.canrnd and ((pygame.time.get_ticks() - self.cooldonw)/1000 >= self.rand):
                
                self.canrnd = False
                # self.color = (255,0,0)
                self.image = pygame.image.load("projek/redcow2.png")
                self.image = pygame.transform.scale(self.image,(100,100)) 
                self.tmp_time = pygame.time.get_ticks()
                self.trigger = True
        
    def pet(self,x):

        if self.trigger :
            if self.rect.collidepoint(x) :
                print('fix')
                self.grade -= (pygame.time.get_ticks() - self.tmp_time)/1000
                self.image = pygame.image.load("projek/cow.png")
                self.image = pygame.transform.scale(self.image,(100,100)) 
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
            print("Correct meat delivered!")
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
        if self.order is None:
            return

        time_left = max(0, (self.wait_limit - (pygame.time.get_ticks() - self.order_time)) // 1000)

        order_surf = self.font.render(f"Order: {self.order}", True, (0, 0, 0))
        time_surf  = self.font.render(f"Time left: {time_left}s", True, (255, 0, 0))

        order_pos = text
        time_pos  = (text[0], text[1] + 30)

        order_rect = order_surf.get_rect(topleft=order_pos)
        time_rect  = time_surf.get_rect(topleft=time_pos)

        frame_rect = order_rect.union(time_rect).inflate(10, 10)

 
        pygame.draw.rect(screen, (255, 255, 255), frame_rect) 

        pygame.draw.rect(screen, (0, 0, 0), frame_rect, 2) 


        screen.blit(order_surf, order_rect.topleft)
        screen.blit(time_surf,  time_rect.topleft)
class meat:
    def __init__(self,x,y,grade,color):
        self.aura = False
        if grade < 5 :
            image = pygame.image.load("projek/meat_rott.png").convert_alpha()
        elif 5 <= grade < 8 :
            image = pygame.image.load("projek/meat.png").convert_alpha()
        else : 
            image = pygame.image.load("projek/neat_aura.png").convert_alpha()
            self.aura = True
  
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
    def __init__(self,prog,screen,root):
        self.default_money = 100
        self.default_game_time = 90
        self.default_score = 0
        self.maxorder = 2
        self.root = root
        
        self.farm = []
        self.meat = []
        self.click = 0
        self.time = 0
        self.posx = 0
        self.posy = 0
        self.score = self.default_score
        self.money = self.default_money
        self.game_time = self.default_game_time
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
        self.screen = screen
        self.prog = prog
        self.drag = None
        
        self.cowslot = 3
        self.currentcow = 1
        self.order = []
        self.mx  = 10
        self.last_recorded_time = 0
        pass
    # def program(self) :

    def helpdraw(self):
        self.screen.fill((255,255,255))
        background = pygame.image.load("projek/คินนิคุแมน_Website_1200x628.jpg").convert()
        self.screen.blit(background, (0, 0))
        self.backgui = pygame.Rect(450,600,300,200)
        self.screen.blit(background, (0, 0))
        # pygame.draw.rect(self.screen,(0,212,255),self.backgui)
        # self.backtomenu = pygame.Rect(300,600,300,100)
        helpmenu = pygame.image.load('projek/backtomenu.png').convert_alpha()
        helpmenu = pygame.transform.scale(helpmenu, (300, 200))
        self.screen.blit(helpmenu,self.backgui.topleft)
        self.howtodum = pygame.Rect(100,100,400,400)
        hwot = pygame.image.load('projek/howtoplay.png').convert_alpha()
        hwot = pygame.transform.scale(hwot, (600, 500))
        self.screen.blit(hwot,self.howtodum.topleft)
    def helpevent(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.backgui.collidepoint(event.pos) :

                self.prog.state = 'menu'
    def menudraw(self):
        self.screen.fill((255,255,255))
        background = pygame.image.load("projek/01kinniku-00a.jpg").convert()
        background = pygame.transform.scale(background,(900,800))
        helpx = 450 - 125
        helpy= 520
        playx = 450 - 175 
        playy = 400
        datax = 450 - 100
        datay = helpy + 100
        settingx = 10
        settingy = 740
        self.setting = pygame.Rect(settingx,settingy,50,50)
        self.helpgui = pygame.Rect(helpx,helpy,250,70)
        self.playgui = pygame.Rect(playx,playy,350,100)
        self.datagui = pygame.Rect(datax,datay,200,70)
        self.logo = pygame.Rect(300,50,300,300)
        logoimg = pygame.image.load("projek/logo.png")
        logoimg =  pygame.transform.scale(logoimg, (300, 300))
        # rice_image = pygame.image.load("projek/rice.png").convert_alpha()
        # self.screen.blit(rice_image,(ricex,ricey))
        # image = pygame.image.load("projek/soiju_2-removebg-preview.png")
        # image = pygame.transform.scale(image, (150, 150))
        self.screen.blit(background, (0, 0))
        # pygame.draw.rect(self.screen,(0,255,0),self.setting)
        # pygame.draw.rect(self.screen,(0,212,255),self.datagui)
        dataimg = pygame.image.load("projek/data.png")
        dataimg =  pygame.transform.scale(dataimg, (200, 70))
        helpimg = pygame.image.load("projek/help.png")
        helpimg =  pygame.transform.scale(helpimg, (250, 100))
        # pygame.draw.rect(self.screen,(0,212,255),self.helpgui)
        # pygame.draw.rect(self.screen,(0,212,255),self.playgui)
        setimg = pygame.image.load("projek/hum.png")
        setimg =  pygame.transform.scale(setimg, (50, 50))

        image = pygame.image.load("projek/button_start.png")
        image = pygame.transform.scale(image, (350, 200))
        self.screen.blit(logoimg,self.logo.topleft)
        self.screen.blit(dataimg,self.datagui.topleft)
        self.screen.blit(image,(playx,playy-50))
        self.screen.blit(setimg,self.setting.topleft)
        self.screen.blit(helpimg,self.helpgui.topleft)
    def menuevent(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.playgui.collidepoint(event.pos) :
                self.reset()
                self.prog.state = 'play'
            if self.helpgui.collidepoint(event.pos) :
                self.prog.state = 'help'
            if self.datagui.collidepoint(event.pos):
                self.launch_stat_graph()
            if self.setting.collidepoint(event.pos) :
                self.prog.state = 'setting'
                
    def settingdraw(self):
        self.screen.fill((255,255,255))
        self.settingmoney = pygame.Rect(50,100,200,75)
        self.settingtime = pygame.Rect(50,200,200,75)
        self.settingscore = pygame.Rect(50,300,200,75)
        font = pygame.font.SysFont('Arial', 36)
        self.screen.blit(font.render(f"your current money :{self.default_money}", True, (0, 0, 0)), (50, 100))
        self.screen.blit(font.render(f"your current time :{self.default_game_time}", True, (0, 0, 0)), (50, 200))
        self.screen.blit(font.render(f"your current score :{self.default_score}", True, (0, 0, 0)), (50, 300))
        self.screen.blit(font.render(f"your Max Oder :{self.maxorder}", True, (0, 0, 0)), (50, 400))
        self.quitbtnsttmn = pygame.Rect(700,700,200,100)
        image = pygame.image.load('projek/button_quit.png').convert_alpha()
        image = pygame.transform.scale(image, (200, 100))
        self.screen.blit(image,self.quitbtnsttmn.topleft)
        tmp = pygame.font.SysFont('Arial', 17)
        self.screen.blit(tmp.render(f"Press arrow up to increase money Press arrow down to decrease money right to add time  left to lowertime", True, (0, 0, 0)), (50, 500))
        self.screen.blit(tmp.render(f"Press s  to increase score Press d down to decrease score C to add max order  V to dercrease max order", True, (0, 0, 0)), (50, 600))
    def settingevent(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.default_money += 100
            elif event.key == pygame.K_DOWN: 
                self.default_money -= 100
            elif event.key == pygame.K_RIGHT:
                self.default_game_time += 10
            elif event.key == pygame.K_LEFT:
                self.default_game_time -= 10
            elif event.key == pygame.K_s:
                self.default_score += 5
            elif event.key == pygame.K_d: 
                self.default_score -= 5
            elif event.key == pygame.K_c:
                self.maxorder += 1
            elif event.key == pygame.K_v: 
                self.maxorder -= 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.quitbtnsttmn.collidepoint(event.pos) :
                self.prog.state = 'menu'
    def play(self):
        if self.game_time <= 0 and self.default_game_time == 90 and self.default_money == 100 and self.default_score == 0:
            
            df = pd.DataFrame(self.mouse_data)
            df[['rel_x', 'rel_y']] = pd.DataFrame(df['rel'].tolist(), index=df.index)
            df['distance'] = np.sqrt(df['rel_x']**2 + df['rel_y']**2)
            total_distance = df['distance'].sum()
            summary_df = pd.DataFrame([{
        'mouse_total_distance': total_distance,
        'click': self.total_click,
        'time': self.total_time,
        'score': self.total_score,
        'cook': self.total_cooked,
        'serve': self.total_serve
    }])
            write_header = not os.path.exists('projek/data.csv')
            summary_df.to_csv('projek/data.csv', mode='a', header=write_header, index=False)
            self.prog.state = 'ending'
        self.screen.fill((255,255,255))
        
        
        self.menu = ['Cooked-Meat-Rice','Cooked-Steak','Medium-rare-Rice','Medium-rare-Steak','Soiju']
        WHITE = (255, 255, 255)
        font = pygame.font.SysFont('Arial', 24)
        RED = (255, 0, 0)
        Blue = (0,255,0)

        
        
        my = 500
        
        pan_color = (0, 200, 255)
        self.pan_pos = (400, 650)
        ricex = 10
        ricey = 300
        self.rice = pygame.Rect(ricex,ricey,200,200)
        rice_image = pygame.image.load("projek/rice.png").convert_alpha()
        quit_image = pygame.image.load('projek/button_quit.png').convert_alpha()
        self.quitbtn = pygame.Rect(700,700,200,100)
        quit_image = pygame.transform.scale(quit_image, (200, 100))
        
        self.buy = pygame.Rect(10, 150, 150, 75)
        buyimg = pygame.image.load("projek/buy.png")
        buyimg = pygame.transform.scale(buyimg,(150,75))
        steakx = 650
        steaky = 350
        self.steak = pygame.Rect(steakx,steaky,200,200)
        steakimg = pygame.image.load("projek/pan-removebg-preview.png")
        steakimg = pygame.transform.scale(steakimg,(200,200))
        soijux = 650
        soijuy = 500
        self.soiju = pygame.Rect(soijux,soijuy,200,200)
        soijuimg = pygame.image.load("projek/keang-removebg-preview.png")
        soijuimg = pygame.transform.scale(soijuimg,(200,200))
        self.pan_radius = 165   
        clock = pygame.time.Clock()
        self.serve = pygame.Rect(280,300,300,300)
        serveimg = pygame.image.load("projek/serve.png")
        serveimg = pygame.transform.scale(serveimg,(300,300))
        cowslotx = 0
        cowsloty = 200
        self.cowslotgui = pygame.Rect(cowslotx,cowsloty,200,100)
        cowsltimg = pygame.image.load("projek/addcowslot.png")
        cowsltimg = pygame.transform.scale(cowsltimg,(200,100))
        trashx = 10
        trashy = 700
        self.trash = pygame.Rect(trashx,trashy,150,150)
        trashimg = pygame.image.load("projek/trashcan.png") 
        trashimg = pygame.transform.scale(trashimg,(150,150))
        self.box = pygame.Rect(10,500,200,200)
        boximg = pygame.image.load("projek/dish.png")
        boximg = pygame.transform.scale(boximg,(200,200))
        delta_time = clock.tick(60)
        # pygame.draw.rect(self.screen,(0,212,255),self.trash)
        # pygame.draw.rect(self.screen,(0,212,255),self.cowslotgui)
        # pygame.draw.rect(self.screen,(0,0,255),self.soiju)
        # pygame.draw.rect(self.screen,(0,0,255),self.steak)
        # pygame.draw.rect(self.screen,(0,255,0),self.serve)
        # pygame.draw.rect(self.screen,(255,0,0),self.buy)
        # pygame.draw.rect(self.screen,(255,0,0),self.box)

        backgroundplay = pygame.image.load("projek/background.png").convert()
        backgroundplay = pygame.transform.scale(backgroundplay,(900,800))
        self.screen.blit(backgroundplay, (0, 0))
        # pygame.draw.circle(self.screen, pan_color, self.pan_pos, self.pan_radius)
        self.screen.blit(boximg,self.box.topleft)
        self.screen.blit(serveimg,self.serve.topleft)
        self.screen.blit(buyimg,self.buy.topleft)
        self.screen.blit(cowsltimg,self.cowslotgui.topleft)
        self.screen.blit(trashimg,self.trash.topleft)
        self.screen.blit(rice_image,(ricex,ricey))
        self.screen.blit(steakimg,self.steak.topleft)
        self.screen.blit(soijuimg,self.soiju.topleft)
        self.screen.blit(quit_image,self.quitbtn.topleft)
        while len(self.order) < self.maxorder :
            tmp2 = random.randrange(70,100)
            custom = customer(tmp2*1000)
            custom.generate_order(self.menu)
            self.order.append(custom)
            # p = order.copy()
        for i in self.order :
            if i.order == None :
                if i.slow == True :
                    self.score -= 0
                self.order.remove(i)
                break
            i.update(self.score)
        for i in range(len(self.order)):
            x = 600 
            y = 50
            dest = (x - (i * 250),y)
                # print(type(dest))
            self.order[i].draw(self.screen,dest)

        for i in self.farm :
            i.update()
            if i.active :                        
                # pygame.draw.rect(self.screen, i.color, i.rect)
                self.screen.blit(i.image,i.rect.topleft)
            else:
                self.currentcow -= 1
                if i.grade > 8 :
                    color = (0,255,0)
                    
                elif 5 <= i.grade < 8 :
                    color = (255,0,0)
                else :
                    color = (0,0,0)
                self.meat.append(meat(self.mx,my,i.grade,color))
                self.farm.remove(i)
                self.mx += 20
                    
                del i
                    
        for i in self.meat:
            if i.show == True :
                    # pygame.draw.rect(screen,i.color,i.rect,0)
                self.screen.blit(i.image,(i.rect.x,i.rect.y))
                i.cook(self.screen, delta_time)
        self.game_time -= delta_time/1000
        # click = font.render(f'{self.total_click}', True, Blue)
        text = font.render(f'Game TIme = {self.game_time:.0f}', True, Blue)
        score = font.render(f'Score = {self.score}', True, Blue)
        money = font.render(f'Money = {self.money}', True, Blue)
        self.screen.blit(text, (600, 100))
        self.screen.blit(score, (600, 200))
        self.screen.blit(money, (600, 300))
        # self.screen.blit(click, (200, 500))
        # print(self.mouse_data)
    def launch_stat_graph(self):
        self.root.after(0, lambda: StatViewer(self.root, "projek/data.csv"))
    def playevent(self,event) :
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.total_click += 1
                if self.buy.collidepoint(event.pos) and (self.currentcow <= self.cowslot) and self.money >= 15:
                    self.money -= 15                       
                    print('addcow')
                    self.posx = 100 * ((self.currentcow-1))
                    self.farm.append(cow(self.posx,self.posy))
                    self.currentcow += 1

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
                if self.quitbtn.collidepoint(event.pos) :
                    self.prog.state = 'menu'
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
                            if self.meat[self.drag].aura :
                                image = pygame.image.load("projek/raw-aura.png")
                                image = pygame.transform.scale(image, (150, 150))
                            else :
                                image = pygame.image.load("projek/raw-removebg-preview.png")
                                image = pygame.transform.scale(image, (150, 150))
                            self.meat[self.drag].image = image.convert_alpha()
                            if self.meat[self.drag].menu == 'Cooked' :
                                self.meat[self.drag].menu += '-Meat-Rice'
                                self.total_cooked += 1 
                            else :
                                self.meat[self.drag].menu += '-Rice'
                                self.total_cooked += 1
                        if self.trash.collidepoint(mouse_pos) :
                            self.meat.remove(self.meat[self.drag]) 
                        if self.steak.collidepoint(mouse_pos)and self.meat[self.drag].menu != None :
                            self.meat[self.drag].permcook = False
                            if self.meat[self.drag].aura :
                                image = pygame.image.load("projek/steakaura.png")
                                image = pygame.transform.scale(image, (150, 150))
                            else :
                                image = pygame.image.load("projek/steabg.png")
                                image = pygame.transform.scale(image, (150, 150))
                            self.meat[self.drag].image = image.convert_alpha()
                            
                            self.meat[self.drag].menu += '-Steak'
                            self.total_cooked += 1
                        if self.soiju.collidepoint(mouse_pos) and self.meat[self.drag].menu == None :
                            self.meat[self.drag].permcook = False

                            if self.meat[self.drag].aura :
                                image = pygame.image.load("projek/soiju_2-aura.png")
                                image = pygame.transform.scale(image, (150, 150))
                            else :
                                image = pygame.image.load("projek/soiju_2-removebg-preview.png")
                                image = pygame.transform.scale(image, (150, 150))
                            self.meat[self.drag].image = image.convert_alpha()
                            self.meat[self.drag].menu = 'Soiju'
                            self.total_cooked += 1
                        if self.serve.collidepoint(mouse_pos) and self.meat[self.drag].menu != None :
                            for i in self.order :
                                
                                crr = i.check_delivery(self.meat[self.drag].menu)
                                bonus = 0
                                if self.meat[self.drag].aura :
                                    bonus = 100
                                if crr :
                                        

                                    self.score += (i.customerscore * (1+(0.1 *(self.meat[self.drag].grade)))) + bonus
                                    self.meat.remove(self.meat[self.drag])

                                    self.game_time += 15
                                    self.total_time += 15
                                    break
                                else : 
                                    self.score -= 30
                                    self.game_time -= 10
                                    self.meat.remove(self.meat[self.drag])
                                    break
                            self.total_serve += 1
                            self.total_score += self.score
                                        

                                        
                        self.drag = None
                            
            if event.type == pygame.MOUSEMOTION:
                if self.drag != None :
                    self.meat[self.drag].rect.move_ip(event.rel)
                current_time = pygame.time.get_ticks()
                if current_time - self.last_recorded_time >= 1000:  # 1000 ms = 1 วิ
                    self.mouse_data.append({
                    "time": current_time,
                    "pos": event.pos,
                    "rel": event.rel
                        })
                    self.last_recorded_time = current_time
    def enddraw(self) :
        self.screen.fill((255,255,255))
        background = pygame.image.load("projek/chara01.png").convert()
        self.screen.blit(background, (0, 0))
        self.newgame_button = pygame.Rect(300,300,300,100)
        newimg = pygame.image.load("projek/repaly.png")
        newimg =  pygame.transform.scale(newimg, (300, 100))
        self.screen.blit(newimg,self.newgame_button.topleft)
        self.backtomenu = pygame.Rect(300,600,300,100)
        quitimage = pygame.image.load('projek/backtomenu.png').convert_alpha()
        quitimage = pygame.transform.scale(quitimage, (300, 100))
        self.screen.blit(quitimage,self.backtomenu.topleft)
        # pygame.draw.rect(self.screen,(0,212,255),self.newgame_button)
        # pygame.draw.rect(self.screen,(0,212,255),self.backtomenu)
        self.graph_button = pygame.Rect(300, 450, 300, 100)
        graphimg = pygame.image.load("projek/data.png")
        graphimg =  pygame.transform.scale(graphimg, (300, 100))
        self.screen.blit(graphimg,self.graph_button.topleft)
        # pygame.draw.rect(self.screen, (255, 100, 100), self.graph_button)
        # font = pygame.font.SysFont('Arial', 36)
        # self.screen.blit(font.render("Show Stats (Graph)", True, (0, 0, 0)), (360, 585))
    def end_event(self,event) :
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.newgame_button.collidepoint(event.pos) :
                self.reset()
                self.prog.state = 'play'
            if self.backtomenu.collidepoint(event.pos) :
                self.prog.state = 'menu'
            if self.graph_button.collidepoint(event.pos):
                self.launch_stat_graph()
    def reset(self):
        self.buy = pygame.Rect(0, 150, 50, 100)
        self.farm = []
        self.meat = []
        self.click = 0
        self.time = 0
        self.posx = 0
        self.posy = 0
        self.score = 5000
        self.score = self.default_score
        self.money = self.default_money
        self.game_time = self.default_game_time
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
        self.drag = None
        self.box = pygame.Rect(100,150,50,50)
        self.cowslot = 3
        self.currentcow = 1
        self.order = []
        self.mx  = 50
        self.last_recorded_time = 0

class Prog() :
    def __init__(self):
        self.screen = pygame.display.set_mode((900,800))
        self.root = tk.Tk()
        self.root.withdraw()
        self.game = game(self,self.screen,self.root)
        self.running = True
        self.state = 'menu'
        
    def run(self) :
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if self.state == "menu":
                    self.game.menuevent(event)
                elif self.state == "play":
                    self.game.playevent(event)
                elif self.state == 'help' :
                    self.game.helpevent(event)
                elif self.state == 'ending' :
                    self.game.end_event(event)
                elif self.state == 'setting':
                    self.game.settingevent(event)
            if self.state == "menu":
                self.game.menudraw()
            elif self.state == "play":
                self.game.play()
            elif self.state == 'help' :
                self.game.helpdraw()
            elif self.state == 'ending' :
                self.game.enddraw()
            elif self.state == 'setting':
                    self.game.settingdraw()
            try:
                self.root.update_idletasks()
                self.root.update()
            except tk.TclError:

                pass
            pygame.display.flip()
if __name__ == '__main__' :

    pygame.init()
    
    a = Prog()
    a.run()


