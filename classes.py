import pygame
from pygame.math import Vector2
from random import *
import math
import numpy as np 

WIDTH = 1200
HEIGHT = 600
SCREEN_SIZE = (WIDTH,HEIGHT)
BOTAO_PLAY_POS = (1200/2 - 256, 600/2 - 254)
#Cores:
BLACK = (0,0,0)
WHITE = (255,255,255)
BROWN = (66,40,14)
GREEN = (0,255,0)

class Jogo:
    """
    Classe que roda o jogo principal em si

    ...

    Attributes
    ----------
    window : armazena a janela do jogo do pygame
    tela_atual : armazena um objeto que representa a tela atual do jogo


    Methods
    -------
    atualiza()
        responsável por parar loop do jogo quando encerrado
    
    game_loop()
        responsável por executar todo o loop do jogo 

    finaliza()
        encerra o pygame 

    """
    def __init__(self):
        """
            Parameters
            ----------
            window : armazena a janela do jogo do pygame
            tela_atual : armazena um objeto que representa a tela atual do jogo

        """
        pygame.init()
        pygame.font.init()
        self.window =  pygame.display.set_mode([WIDTH,HEIGHT])
        pygame.display.set_caption("Cosmic Chaos")

        self.tela_atual = Tela_inicio()
        
    def atualiza(self):

        self.tela_atual = self.tela_atual.atualiza()

        if self.tela_atual is None:
            return False
        return True
    
    def game_loop(self):
        while self.atualiza():
            self.tela_atual.desenha(self.window)
            pygame.display.update()
    
    def finaliza(self):
        pygame.quit()



class Tela_inicio():
    """
    Classe que roda a tela inicial

    ...

    Attributes
    ----------
    tela_inicio : png da tela inicial
    rect_botao_play : define os limites do botão de play
    rect_regras : define os limites do botão de ler as regras


    Methods
    -------
    atualiza()
        responsável por parar loop do jogo quando encerrado e computar outros eventos da tela
    
    desenha()
        responsável por desenhar todos os atríbutos da tela

    """
    def __init__(self):
        self.tela_inicio = pygame.image.load('Assets/Cosmic_Chaos.png').convert_alpha()
        self.rect_botao_play = (455,214,256,226)
        self.rect_regras = (347,461,477,100)
        
        
    
    def atualiza(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if colisao_ponto_retangulo(event.pos[0],event.pos[1], self.rect_botao_play):   
                        return Level0()
                    elif colisao_ponto_retangulo(event.pos[0],event.pos[1], self.rect_regras):   
                        return Tela_regras()

        
        return self    
                
    def desenha(self,surface):
        FONTE = pygame.font.Font('Fonts/SERIO___.TTF',20) 
        surface.fill(BLACK)
        surface.blit(self.tela_inicio,(0,0))

class Tela_regras():
    """
    Classe que roda a tela de regras

    ...

    Attributes
    ----------
    tela_regras : png da tela de regras
    rect_back : define os limites do botão de voltar a tela inicial


    Methods
    -------
    atualiza()
        responsável por parar loop do jogo quando encerrado e computar outros eventos da tela
    
    desenha()
        responsável por desenhar todos os atríbutos da tela

    """
    def __init__(self):
        self.tela_regras = pygame.image.load('Assets/regras.png').convert_alpha()
        self.rect_back = (1065,505,135,100)
        
        
    
    def atualiza(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if colisao_ponto_retangulo(event.pos[0],event.pos[1], self.rect_back):   
                        return Tela_inicio()

        
        return self    
                
    def desenha(self,surface):
        FONTE = pygame.font.Font('Fonts/SERIO___.TTF',20) 
        surface.fill(BLACK)
        surface.blit(self.tela_regras,(0,0))

class Level0():
    """
    Classe que roda a primeira fase 

    ...

    Attributes
    ----------
    qtd_tiros : usado para contar o limite máximo de tiros (3)
    pos_planetas : pos dos planetas no png das sprites
    lista_tiros : armazena os objetos de tiro presentes na tela (max 1)
    space_shooter : armazena o objeto da classe SpaceShooter (canhão responsável por atirar)
    background : armazena o png do fundo da tela
    tiro_mini : png do tiro pequeno que fica acima marcando os tiros ainda disponíveis 
    lista_planetas : armazena os objetos da classe Planeta presentes na fase
    lista_satelite : armazena os objetos da classe Satelite presentes na fase


    Methods
    -------
    atualiza()
        responsável por parar loop do jogo quando encerrado e computar outros eventos da tela
    
    desenha()
        responsável por desenhar todos os atríbutos da tela

    """
    def __init__(self): 
        self.qtd_tiros = 3
        self.pos_planetas = {'terra':(49,53,83,77),'netuno':(154,56,82,75),'marte':(48,162,85,79)}
        self.lista_tiros = []
        self.space_shooter = SpaceShooter()
        self.background = pygame.image.load('Assets/space_background.png').convert_alpha()
        self.tiro_mini = pygame.image.load('Assets/tiro_mini.png').convert_alpha()
        self.lista_planetas = [Planeta(self.pos_planetas['terra'],[600-83,300-77],50000)]
        self.lista_satelite = [Satellite([1000,200])]
        
    
    def atualiza(self):

        mx, my = pygame.mouse.get_pos()
        self.space_shooter.mx,self.space_shooter.my = mx,my

        for planeta in self.lista_planetas:
            if len(self.lista_tiros) > 0:
                a = - planeta.gravidade(self.lista_tiros[0].pos)
                if np.linalg.norm(planeta.pos - self.lista_tiros[0].pos) <= (planeta.pos_sprites[2]/2) + (self.lista_tiros[0].w/2):
                    self.lista_tiros.remove(self.lista_tiros[0])

        if len(self.lista_tiros) > 0:
            for tiro in self.lista_tiros:
                x = tiro.atualiza(pygame.Rect(self.lista_satelite[0].pos[0],self.lista_satelite[0].pos[1],55,55),a) #55,55 eh o w,h do sattelite mas apenas dele e nao da img
                if not x:
                    self.lista_tiros.remove(self.lista_tiros[0])
                elif x == 'acabou': #mexendo aqui pra acabar
                    return Level1()

        self.lista_satelite[0].atualiza()

        if len(self.lista_tiros) == 0 and self.qtd_tiros == 0:
            return Tela_Perdeu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if len(self.lista_tiros) < 1:
                        self.lista_tiros.append(Tiro([mx,my],[self.space_shooter.rot_image_rect.centerx - 22,self.space_shooter.rot_image_rect.centery - 22]))
                        self.qtd_tiros -= 1
        return self    
    
                
    def desenha(self,surface):
        FONTE = pygame.font.Font('Fonts/SERIO___.TTF',25) 
        surface.fill(BLACK)
        surface.blit(self.background,(0,0))

        texto_level = FONTE.render('LEVEL 1', True, WHITE) 
        surface.blit(texto_level,(1100,0))
        
        if self.qtd_tiros >= 3:
            surface.blit(self.tiro_mini,(70,10))
        if self.qtd_tiros >= 2:
            surface.blit(self.tiro_mini,(35,10))
        if self.qtd_tiros >= 1:
            surface.blit(self.tiro_mini,(0,10))
        

        for tiro in self.lista_tiros:
            tiro.desenha(surface)

        self.space_shooter.desenha(surface)

        for planeta in self.lista_planetas:
            planeta.desenha(surface)

        for sat in self.lista_satelite:
            sat.desenha(surface)



class Level1():
    """
    Classe que roda a segunda fase 

    ...

    Attributes
    ----------
    qtd_tiros : usado para contar o limite máximo de tiros (3)
    pos_planetas : pos dos planetas no png das sprites
    lista_tiros : armazena os objetos de tiro presentes na tela (max 1)
    space_shooter : armazena o objeto da classe SpaceShooter (canhão responsável por atirar)
    background : armazena o png do fundo da tela
    tiro_mini : png do tiro pequeno que fica acima marcando os tiros ainda disponíveis 
    lista_planetas : armazena os objetos da classe Planeta presentes na fase
    lista_satelite : armazena os objetos da classe Satelite presentes na fase


    Methods
    -------
    atualiza()
        responsável por parar loop do jogo quando encerrado e computar outros eventos da tela
    
    desenha()
        responsável por desenhar todos os atríbutos da tela

    """
    def __init__(self): 
        self.qtd_tiros = 3
        self.pos_planetas = {'terra':(49,53,83,77),'netuno':(154,56,82,75),'marte':(48,162,85,79)}
        self.lista_tiros = []
        self.space_shooter = SpaceShooter()
        self.background = pygame.image.load('Assets/space_background.png').convert_alpha()
        self.tiro_mini = pygame.image.load('Assets/tiro_mini.png').convert_alpha()
        self.lista_planetas = [Planeta(self.pos_planetas['terra'],[600,250],5000),Planeta(self.pos_planetas['netuno'],[800,150], 1000),Planeta(self.pos_planetas['marte'],[800,500],2000)]
        self.lista_satelite = [Satellite([1000,200])]
        
    
    def atualiza(self):

        mx, my = pygame.mouse.get_pos()
        self.space_shooter.mx,self.space_shooter.my = mx,my

        a = 0

        for planeta in self.lista_planetas:
            if len(self.lista_tiros) > 0:
                a -= planeta.gravidade(self.lista_tiros[0].pos)
                if np.linalg.norm(planeta.pos - self.lista_tiros[0].pos) <= ((planeta.pos_sprites[2]/2) + (self.lista_tiros[0].w/2) - 25):
                    self.lista_tiros.remove(self.lista_tiros[0])


        if len(self.lista_tiros) > 0:
            for tiro in self.lista_tiros:
                x = tiro.atualiza(pygame.Rect(self.lista_satelite[0].pos[0],self.lista_satelite[0].pos[1],55,55),a) 
                if not x:
                    self.lista_tiros.remove(self.lista_tiros[0])
                elif x == 'acabou': 
                    return Level2()

        self.lista_satelite[0].atualiza()

        if len(self.lista_tiros) == 0 and self.qtd_tiros == 0:
            return Tela_Perdeu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if len(self.lista_tiros) < 1:
                        self.lista_tiros.append(Tiro([mx,my],[self.space_shooter.rot_image_rect.centerx - 22,self.space_shooter.rot_image_rect.centery - 22]))
                        self.qtd_tiros -= 1
        return self    
    
                
    def desenha(self,surface):
        FONTE = pygame.font.Font('Fonts/SERIO___.TTF',25) 
        surface.fill(BLACK)
        surface.blit(self.background,(0,0))

        texto_level = FONTE.render('LEVEL 2', True, WHITE) 
        surface.blit(texto_level,(1100,0))
        
        if self.qtd_tiros >= 3:
            surface.blit(self.tiro_mini,(70,10))
        if self.qtd_tiros >= 2:
            surface.blit(self.tiro_mini,(35,10))
        if self.qtd_tiros >= 1:
            surface.blit(self.tiro_mini,(0,10))
        

        for tiro in self.lista_tiros:
            tiro.desenha(surface)

        self.space_shooter.desenha(surface)

        for planeta in self.lista_planetas:
            planeta.desenha(surface)

        for sat in self.lista_satelite:
            sat.desenha(surface)

class Level2():
    """
    Classe que roda a terceira e última fase 

    ...

    Attributes
    ----------
    qtd_tiros : usado para contar o limite máximo de tiros (3)
    pos_planetas : pos dos planetas no png das sprites
    lista_tiros : armazena os objetos de tiro presentes na tela (max 1)
    space_shooter : armazena o objeto da classe SpaceShooter (canhão responsável por atirar)
    background : armazena o png do fundo da tela
    tiro_mini : png do tiro pequeno que fica acima marcando os tiros ainda disponíveis 
    lista_planetas : armazena os objetos da classe Planeta presentes na fase
    lista_satelite : armazena os objetos da classe Satelite presentes na fase


    Methods
    -------
    atualiza()
        responsável por parar loop do jogo quando encerrado e computar outros eventos da tela
    
    desenha()
        responsável por desenhar todos os atríbutos da tela

    """
    def __init__(self):  
        self.qtd_tiros = 3
        self.pos_planetas = {'terra':(49,53,83,77),'netuno':(154,56,82,75),'marte':(48,162,85,79),'saturno':(240,385,125,48),'jupiter':(262,164,83,76)}
        self.lista_tiros = []
        self.space_shooter = SpaceShooter()
        self.background = pygame.image.load('Assets/space_background.png').convert_alpha()
        self.tiro_mini = pygame.image.load('Assets/tiro_mini.png').convert_alpha()
        self.lista_planetas = [Planeta(self.pos_planetas['terra'],[300,100],5000),Planeta(self.pos_planetas['netuno'],[450,450],1000),Planeta(self.pos_planetas['marte'],[700,200],2500),Planeta(self.pos_planetas['saturno'],[780,450],7500)]
        self.lista_satelite = [Satellite([1000,200])]
        
    
    def atualiza(self):

        mx, my = pygame.mouse.get_pos()
        self.space_shooter.mx,self.space_shooter.my = mx,my

        a = 0

        for planeta in self.lista_planetas:
            if len(self.lista_tiros) > 0:
                a -= planeta.gravidade(self.lista_tiros[0].pos)
                if np.linalg.norm(planeta.pos - self.lista_tiros[0].pos) <= (planeta.pos_sprites[3]/2) + (self.lista_tiros[0].w/2):
                    self.lista_tiros.remove(self.lista_tiros[0])


        if len(self.lista_tiros) > 0:
            for tiro in self.lista_tiros:
                x = tiro.atualiza(pygame.Rect(self.lista_satelite[0].pos[0],self.lista_satelite[0].pos[1],55,55),a) 
                if not x:
                    self.lista_tiros.remove(self.lista_tiros[0])
                elif x == 'acabou': 
                    return Tela_Ganhou()

        self.lista_satelite[0].atualiza()

        if len(self.lista_tiros) == 0 and self.qtd_tiros == 0:
            return Tela_Perdeu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if len(self.lista_tiros) < 1:
                        self.lista_tiros.append(Tiro([mx,my],[self.space_shooter.rot_image_rect.centerx - 22,self.space_shooter.rot_image_rect.centery - 22]))
                        self.qtd_tiros -= 1
        return self    
    
                
    def desenha(self,surface):
        FONTE = pygame.font.Font('Fonts/SERIO___.TTF',25) 
        surface.fill(BLACK)
        surface.blit(self.background,(0,0))

        texto_level = FONTE.render('LEVEL 2', True, WHITE) 
        surface.blit(texto_level,(1100,0))
        
        if self.qtd_tiros >= 3:
            surface.blit(self.tiro_mini,(70,10))
        if self.qtd_tiros >= 2:
            surface.blit(self.tiro_mini,(35,10))
        if self.qtd_tiros >= 1:
            surface.blit(self.tiro_mini,(0,10))
        

        for tiro in self.lista_tiros:
            tiro.desenha(surface)

        self.space_shooter.desenha(surface)

        for planeta in self.lista_planetas:
            planeta.desenha(surface)

        for sat in self.lista_satelite:
            sat.desenha(surface)

class Tela_Perdeu():
    """
    Classe que roda a tela após o jogador perder 

    ...

    Attributes
    ----------
    tela_perdeu : png da tela de derrota
    rect_play : define os limites do botão de jogar novamente
    back_to_inicio : define os limites do botão de retornar ao menu
    


    Methods
    -------
    atualiza()
        responsável por parar loop do jogo quando encerrado e computar outros eventos da tela
    
    desenha()
        responsável por desenhar todos os atríbutos da tela

    """
    def __init__(self):
        self.tela_perdeu = pygame.image.load('Assets/perdeu.png').convert_alpha()
        self.rect_play = [485,252,227,202]
        self.back_to_inicio = [247,505,709,54]
        
    
    def atualiza(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if colisao_ponto_retangulo(event.pos[0],event.pos[1], self.rect_play):   
                        return Level0()
                    if colisao_ponto_retangulo(event.pos[0],event.pos[1], self.back_to_inicio):
                        return Tela_inicio()
        return self    
                
    def desenha(self,surface):
        FONTE = pygame.font.Font('Fonts/SERIO___.TTF',20) 
        surface.fill(BLACK)
        surface.blit(self.tela_perdeu,(0,0))

class Tela_Ganhou():
    """
    Classe que roda a tela após o jogador perder 

    ...

    Attributes
    ----------
    tela_ganhou : png da tela de derrota
    rect_play : define os limites do botão de jogar novamente
    back_to_inicio : define os limites do botão de retornar ao menu
    


    Methods
    -------
    atualiza()
        responsável por parar loop do jogo quando encerrado e computar outros eventos da tela
    
    desenha()
        responsável por desenhar todos os atríbutos da tela

    """
    def __init__(self):
        self.tela_ganhou = pygame.image.load('Assets/ganhou.png').convert_alpha()
        self.rect_play = [485,252,227,202]
        self.back_to_inicio = [247,505,709,54]
        
    
    def atualiza(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if colisao_ponto_retangulo(event.pos[0],event.pos[1], self.rect_play):   
                        return Level0()
                    if colisao_ponto_retangulo(event.pos[0],event.pos[1], self.back_to_inicio):
                        return Tela_inicio()
        return self    
                
    def desenha(self,surface):
        FONTE = pygame.font.Font('Fonts/SERIO___.TTF',20) 
        surface.fill(BLACK)
        surface.blit(self.tela_ganhou,(0,0))
#-------------------------------------------------------#
class SpaceShooter():
    """
    Classe que gera o objeto do canhão presente na fase

    ...

    Attributes
    ----------
    player : png do objeto
    player_pos : armazena a posição inicial do objeto
    rot_image : armazena a posição após rotacionado do objeto
    player_rect : armazena os limites do objeto
    rot_image_rect : armazena os limites do objeto depois de rotacionado 
    mx,my : posição do mouse na tela armazenada
    w,h : armazena largura e altura do objeto
    angle : armazena o angulo se o objeto rotacionado
    


    Methods
    -------
    atualiza()
        responsável por parar loop do jogo quando encerrado e computar outros eventos da tela
    
    desenha()
        responsável por desenhar o objeto SpaceShooter, e também realiza a rotação se necessária de acordo com o mx,my

    """
    def __init__(self):
        self.player = pygame.image.load("Assets/space-fighter.png").convert_alpha()
        self.player_pos = ''
        self.player_rect = ''
        self.rot_image = ''
        self.rot_image_rect = ''
        self.mx = 0
        self.my = 0

        self.w = 120
        self.h = 120
        self.angle = 0
    

    def desenha(self,surface):
        self.player_pos  = (80,525)
        self.player_rect = self.player.get_rect(center = self.player_pos)

        dx, dy = self.mx - self.player_rect.centerx, self.my - self.player_rect.centery

        a = math.degrees(math.atan2(-dy, dx)) - 90
        if a > -100 and a <= 10:
            self.angle = math.degrees(math.atan2(-dy, dx)) - 90

        self.rot_image = pygame.transform.rotate(self.player, self.angle)
        self.rot_image_rect = self.rot_image.get_rect(center = self.player_rect.center)

        surface.blit(self.rot_image, self.rot_image_rect.topleft)

class Tiro():
    """
    Classe que gera o objeto do tiro presente na fase

    ...

    Attributes
    ----------
    tiro : png do objeto
    w,h : armazena largura e altura do objeto
    velocidade : armazena a velocidade que é constantemente atualizada de acordo com a gravidade
    pos: array que armazena a posição atual do tiro
    mouse_pos : armazena o vetor da posição clicada no mouse
    distance : armazena e calcula a distância do tiro em relação ao click do mouse
    direction : dita a direção em que o objeto tem que se deslocar]
    aceleracao : aceleração que o objeto possui (essencial pois é alterada quando em contato com a gravidade dos planetas)
     angle : armazena o angulo se o objeto rotacionado
    


    Methods
    -------
    atualiza()
        responsável por atualizar o tiro, tanto removelo quando sair dos limites do jogo 
        e também calcular a direção, sentido e velocidade nova quando afetado pela gravidade
    
    desenha()
        responsável por desenhar o objeto Tiro na tela

    """
    def __init__(self,mouse_pos,space_pos):
        self.tiro_img = pygame.image.load('Assets/tiro.png').convert_alpha()
        self.w = 45
        self.h = 45
        self.velocidade = 0.05
        self.pos = np.array([space_pos[0],space_pos[1]]) 
        self.mouse_pos = mouse_pos
        self.distance = math.sqrt((mouse_pos[0] - self.pos[0]) ** 2 + (mouse_pos[1] - self.pos[1]) ** 2)
        self.direction = [(mouse_pos[0] - self.pos[0]) / self.distance, (mouse_pos[1] - self.pos[1]) / self.distance]
        self.aceleracao = 0

        self.angle = 0
    
    def atualiza(self,sat_rect,aceleracao):
        rect = pygame.Rect(self.pos[0],self.pos[1],self.w,self.h)
        if sat_rect.colliderect(rect):
            return 'acabou'
        else:
            self.velocidade = self.direction
            self.pos = self.pos + self.velocidade - aceleracao[0]

            if self.pos[0] >= 1200 or self.pos[0] <= 0 or self.pos[1] <= 0 or self.pos[1] >= 600:
                return False
            return True
    

    def desenha(self,surface):
        surface.blit(self.tiro_img, self.pos)

class Planeta:
    """
    Classe que gera o objeto do tiro presente na fase

    ...

    Attributes
    ----------
    sprites_plan : png das sprites dos planetas
    pos_sprites : armazena a posição do planeta no png de sprites
    pos : array que armazena a posição atual do planeta
    


    Methods
    -------
    gravidade()
        função onde é implementada formula da gravidade (g = (G * M) / d²) e 
        seu efeito sobre o tiro
    
    desenha()
        responsável por desenhar o objeto Tiro na tela
    """
    def __init__(self,pos_sprite,pos,grav=0):
        self.sprites_plan = pygame.image.load("Assets/sprites_planeta.png").convert_alpha()
        self.pos_sprites = pos_sprite
        self.pos = pos
        self.grav = grav

    def desenha(self, surface):
        surface.blit(self.sprites_plan,self.pos,self.pos_sprites)

    def gravidade(self, tiro_pos):
        direction_a = self.pos - tiro_pos
        d = np.linalg.norm(direction_a)
        direction_a = direction_a / d
        mag_a = self.grav / d**2
        a = direction_a * mag_a
        return a
    
class Satellite():
    """
    Classe que gera o objeto do tiro presente na fase

    ...

    Attributes
    ----------
    sat : png do satelite
    pos : array que armazena a posição atual do planeta
    descendo : booleano utilizado para ditar para qual sentido na vertical ele deve se deslocar
    w,h : armazena largura e altura do objeto


    Methods
    -------
    atualiza()
        função que atualiza a posição do satelite, além de também alterar se necessário o seu sentido de deslocamento
    
    desenha()
        responsável por desenhar o objeto Tiro na tela
    """
    def __init__(self,pos):
        self.sat = pygame.image.load("Assets/satellite.png").convert_alpha()
        self.pos = pos
        self.descendo = True
        self.w = 124
        self.h = 73
    
    def atualiza(self,):
        if self.pos[1] >= 500:
            self.descendo = False
        elif self.pos[1] <= 100:
            self.descendo = True

        if self.descendo:
            self.pos[1] += 0.5
        else:
            self.pos[1] -= 0.5

    def desenha(self,surface):
        surface.blit(self.sat, self.pos)



#-----------------------FUNÇÕES--------------------------#
def colisao_ponto_retangulo(ponto_x,ponto_y, rect):
    if ponto_x >= rect[0] and ponto_x <= rect[0] + rect[2]:
        if ponto_y >= rect[1] and ponto_y <= rect[1] + rect[3]:
            return True
    return False

def colisao_rect(r1, r2):
    if r1[0] <= r2[0] + r2[2] and r1[0] + r1[2] >= r2[0] and r1[1] <= r2[1] + r2[3] and r1[1] + r1[3] >= r2[1]:
        return True
    return False