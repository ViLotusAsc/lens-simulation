import pygame 
import math 
from math import atan2, degrees, pi

pygame.init()
desktop_size = pygame.display.get_desktop_sizes()
screen = pygame.display.set_mode((desktop_size[0][0]-10, desktop_size[0][1]-10), pygame.RESIZABLE)


class visualMd:
    def __init__(self) -> None:
        self.font = pygame.sysfont.SysFont("Arial", 15, italic=True)
        
    def text(self):
        font = pygame.sysfont.SysFont("Arial", 30, italic=True)
        screen.blit(font.render("Características da imagem:", True, (0, 0, 0)), (89, 50))

    def create_lines(self):         # Criar as linhas na tela 
        counter_h = 0
        counter_v = 0
        self.lines_hor = []
        self.lines_ver = []
        counter_nmb = 0
        self.list_nmb = [18, 16, 14, 12, 10, 8, 6, 4, 2, -2, -4, -6, -8, -10, -12, -14, -16, -18, -20]
        self.counter_str = 0
        for pixel in range(0, desktop_size[0][1]):
            counter_h += 1
            if counter_h == 40:
                self.lines_hor.append(pixel)
                counter_h = 0
        for pixel in range(0, desktop_size[0][0]):
            counter_v += 1
            if counter_v == 40:
                self.lines_ver.append(pixel)
                counter_v = 0

        for pixel in self.lines_hor:
            pygame.draw.line(screen, (0, 0, 0), (0, pixel), (desktop_size[0][0], pixel), 1)

        for pixel in self.lines_ver:
            pygame.draw.line(screen, (0, 0, 0), (pixel, 0), (pixel, desktop_size[0][1]))
            if counter_nmb == 2:
                pygame.draw.circle(screen, (0, 0, 0), (pixel, 559), 5)
                screen.blit(self.font.render(str(self.list_nmb[self.counter_str]), True, (0, 0, 0)), (pixel, 579))
                counter_nmb = 0
                self.counter_str += 1
            counter_nmb += 1

        
        pygame.draw.line(screen, (0, 0, 0), (0, 559), (desktop_size[0][0], 559), 5) # horizontal
        pygame.draw.line(screen, (0, 0, 0), (800, 0), (800, desktop_size[0][1]), 5) # vertical


class Object:
    def __init__(self, x, y) -> None:
        self.x_pos = x
        self.y_pos = y
        self.y_final = self.y_pos - 100
        self.x_final = self.x_pos
        self.mr = False

    def object(self, cont):     # Visual Object
        if not self.mr:
            pygame.draw.line(screen, (0, 0, 200), (self.x_final, self.y_pos), (self.x_final, self.y_final), 6)
            self.ballContact = pygame.Rect((self.x_final-25, self.y_final-25), (50, 50))
            pygame.draw.circle(screen, (0, 0, 200), (self.x_final, self.y_final), 25, 3)
        else:
            pygame.draw.line(screen, (0, 0, 200), (pygame.mouse.get_pos()[0], self.y_pos), (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]), 6)
    
    
    def light_lines(self, foco_cor, act):        # Light Lines
        if not self.mr:
            pygame.draw.line(screen, (0, 0, 0), (self.x_final,self.y_final), (800, self.y_final), 3) # reta
            pygame.draw.line(screen, (0, 0, 0), (self.x_final, self.y_final), (799, 558), 3) # diagonal
            pygame.draw.line(screen, (0, 0, 0), (self.x_final, self.y_final), foco_cor, 3) # foco
            pygame.draw.line(screen, (0, 0, 0), (800, self.y_final), (800 + (800 - foco_cor[0]), foco_cor[1]), 3)
        else:
            pygame.draw.line(screen, (0, 0, 0), (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]), (800, pygame.mouse.get_pos()[1]), 3) # normal
            pygame.draw.line(screen, (0, 0, 0), (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]), (799, 558), 3) # diagonal
            pygame.draw.line(screen, (0, 0, 0), pygame.mouse.get_pos(), foco_cor, 3)
        if act:
            pygame.draw.line(screen, (0, 0, 0), pygame.mouse.get_pos(), foco_cor, 3)

        dx = self.x_final - 800
        dy = self.y_final - 559
        rads = atan2(-dy, dx)
        rads %= 2*pi
        self.degs = degrees(rads)



class Foco:
    def __init__(self) -> None:
        self.y_pos = 559
        self.x_pos = 300
        self.mr = False

    def foco(self):
        self.ballContact = pygame.Rect((self.x_pos-25, self.y_pos-25), (50, 50))
        # distance_x = 800 - self.x_pos
        if not self.mr:
            pygame.draw.circle(screen, (200, 0, 0), (800 + (800 - self.x_pos), self.y_pos), 10)
            pygame.draw.circle(screen, (200, 0, 0), (self.x_pos, self.y_pos), 25, 3)
        else:
            pygame.draw.circle(screen, (200, 0, 0), (800 + (800 - pygame.mouse.get_pos()[0]), self.y_pos), 10)
            pygame.draw.circle(screen, (200, 0, 0), (pygame.mouse.get_pos()[0], 559), 25, 3)


visual = visualMd()
objeto = Object(700, 559)
foco = Foco()

mr = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if objeto.ballContact.collidepoint(event.pos):
                objeto.mr = True
            if foco.ballContact.collidepoint(event.pos):
                foco.mr = True
            print(event.pos)
            print(objeto.degs)
        if event.type == pygame.MOUSEBUTTONUP:
            if objeto.mr:
                objeto.x_final = pygame.mouse.get_pos()[0]
                objeto.y_final = pygame.mouse.get_pos()[1]
            objeto.mr = False
            if foco.mr:
                foco.x_pos = pygame.mouse.get_pos()[0]
            foco.mr = False
    
    screen.fill((255, 255, 255))
    visual.create_lines()
    visual.text()
    objeto.object(mr)
    objeto.light_lines((foco.x_pos, foco.y_pos), foco.mr)
    foco.foco()
    pygame.display.update()