#/usr/bin/env python
# -*- coding: utf-8 -*-

# Importy
import sys
import os
import pygame
from pygame.locals import *
from random import randint

# Definice třídy mravence
class mravenec:
    def __init__(self, x, y):
        ''' Konstruktor, mravenec dostane souřadnice na kterých se má narodit. '''
        self.x=x
        self.y=y
        self.ma_tycinku=False
    
    def rekni_pozici(self):
        ''' Mravenec vrátí svojí aktuální pozici. '''
        return([self.x, self.y])
    
    def rekni_pozici_x(self):
        ''' Mravenec vrátí svojí aktuální pozici X '''
        return(self.x)
    
    def rekni_pozici_y(self):
        ''' Mravenec vrátí svojí aktuální pozici Y '''
        return(self.y)
    
    def soused(self, coords, smer):
        ''' Vrací vedlejší poličko z aktuálních souřadnic [coords] ve směru [smer]. 
            (Zajišťuje zacyklování pole.) '''
        x=coords[0]
        y=coords[1]
        if smer=="d":
            if y==1: y=y_max+1
            y-=1
        elif smer=="u":
            if y==y_max: y=0
            y+=1
        elif smer=="l":
            if x==1: x=x_max+1
            x-=1
        elif smer=="r":
            if x==x_max: x=0
            x+=1
        return [x,y]
    
    def pohni_se(self):
        ''' Nechá mravence udělat jeden krok pseudonáhodným směrem. '''
        smer = randint(0,3)
        smery = ["u", "d", "l", "r"]
        newc = self.soused(self.rekni_pozici(), smery[smer])    
        self.x=newc[0]
        self.y=newc[1]
        self.uvazuj_nad_tycinkou()
        
    def uvazuj_nad_tycinkou(self):
        ''' Řeší mravencovu interakci s kupičkou tyčinek, kterou (ne)našel. '''
        pozice = self.rekni_pozici()
        tycinky_tady = pole_tycinek[pozice[1]-1][pozice[0]-1]
        
        if tycinky_tady==0:
            pass
        else:
            if self.ma_tycinku:
                self.ma_tycinku = False
                pole_tycinek[pozice[1]-1][pozice[0]-1]+=1
            else:
                self.ma_tycinku = True
                pole_tycinek[pozice[1]-1][pozice[0]-1]-=1

# Definice neznámých
pole_tycinek = []       # Dvourozměrné pole
pole_mravencu = []      # Jednorozěrné pole

# Rozměry pole
x_max=10
y_max=10

# Parametry simulace
pocet_mravencu = 5
pocet_tycinek =400
pocet_obrazku_tycinek = 3
fps = 40
sirka_okna = 500
vyska_okna = 500
save = False

# Generuji mravence a jejich souřadnice
for a in range(0,pocet_mravencu):
    x = randint(1, x_max)
    y = randint(1, y_max)
    pole_mravencu.append(mravenec(x, y))

# Generuji pole tyčinek
for ve_sloupci in range(0,y_max):
    pole_tycinek.append([])
for radek in pole_tycinek:
    for v_radku in range(0,x_max):
        radek.append(0)

# Náhodně rozsypávám tyčinky  
for tycinka in range(0,pocet_tycinek+1):
    sloupec = randint(0,y_max-1)
    radek = randint(0,x_max-1)
    pole_tycinek[sloupec][radek]+=1


pygame.init()
fps_clock = pygame.time.Clock()

# Vyrábím pygame okno
window = pygame.display.set_mode((sirka_okna, vyska_okna)) 

# Nastavuji mu popisek
pygame.display.set_caption('Ant Simulator') 

# Nastavuji ikonku okna
o = pygame.image.load(os.path.join('data/bigant.png')).convert_alpha()
o = pygame.transform.rotate(o, 45)
o = pygame.transform.smoothscale(o, (30, 30))
pygame.display.set_icon(o)

white_color = pygame.Color(255, 255, 255)

ant_surface_object = []
for i in range(0,4):
    o = pygame.image.load(os.path.join('data/bigant.png')).convert_alpha()
    o = pygame.transform.smoothscale(o, ((sirka_okna-30)/x_max, (vyska_okna-30)/y_max))
    ant_surface_object.append(pygame.transform.rotate(o, i*90))

raw_surface_object = []
stick_surface_object = []
for a in range (0,pocet_obrazku_tycinek):
    raw_surface_object.append(pygame.image.load(os.path.join('data/bigstick'+str(a)+'.png')).convert_alpha())
for a in range (0,pocet_tycinek):
    o = pygame.transform.rotate(raw_surface_object[a%pocet_obrazku_tycinek], ((180/19)*3*a))
    o = pygame.transform.smoothscale(o, ((sirka_okna-30)/x_max, (vyska_okna-30)/y_max))
    stick_surface_object.append(o)
    
# Hlavní iterace - každý cyklus je jeden krok
i = 0
while True: 
    # Vyplním okno bílou barvou (reset)
    window.fill(white_color) 
    
    # Vykreslím do okna tyčinky
    r = 1
    s = 1
    for radek in pole_tycinek:
        for sloupec in radek:
            if sloupec > 0:
                for a in range(0,sloupec):
                    window.blit(stick_surface_object[a%pocet_tycinek], ((s-1)*(sirka_okna/(x_max)), (r-1)*(vyska_okna/(y_max))))
            s+=1
        s=1
        r+=1    
    
    # Vykreslím do okna mravence
    for mravenec in pole_mravencu:
        # Zjistím si starou pozici mravence
        oldx = mravenec.rekni_pozici_x()
        oldy = mravenec.rekni_pozici_y()
        
        # Požádám mravence, aby se pohnul
        mravenec.pohni_se()
        
        # Zjistím si novou pozici mravence
        x = mravenec.rekni_pozici_x()
        y = mravenec.rekni_pozici_y()
        
        # Zařídím správné nasměrování mravenců po pohybu
        if ((x==oldx+1) or (x==oldx-(x_max-1))): way=3
        elif ((x==oldx-1) or (x==oldx+(x_max-1))): way=1
        elif ((y==oldy+1) or (y==oldy-(y_max-1))): way=2
        elif ((y==oldy-1) or (y==oldy+(y_max-1))): way=0
        else: way=0
        
        # Vykreslím mravence ve správném směru
        window.blit(ant_surface_object[way], ((x-1)*(sirka_okna/(x_max)), (y-1)*(vyska_okna/(y_max))))
    
    # Uložím obrázek aktuální mapy
    if save:
        pygame.image.save(window, "save/test"+str(i)+".png")
        i+=1
        
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            sys.exit(0) 
        else: 
            pass
            #print event 

    pygame.display.update()
    fps_clock.tick(fps)