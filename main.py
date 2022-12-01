import pygame
import math
import random

pygame.init()

sw = 800
sh = 800

# adicionando imagens
bg = pygame.image.load('asteroidsPics/starbg.png')
playerRocket = pygame.image.load('asteroidsPics/nave.png')
estrela = pygame.image.load('asteroidsPics/estrela.png')
asteroid50 = pygame.image.load('asteroidsPics/asteroid50.png')
asteroid100 = pygame.image.load('asteroidsPics/asteroid100.png')
asteroid150 = pygame.image.load('asteroidsPics/asteroid150.png')

pygame.display.set_caption('Asteroids')
ganhar = pygame.display.set_mode((sw, sh))
timer = pygame.time.Clock()

fimdejogo = False
vidas = 3
pontuacao = 0
rapidFire = False
rfStart = -1
maximapontuacao = 0

#funçoes da nave
class Player(object):
    def __init__(self):
        self.img = playerRocket
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.x = sw//2
        self.y = sh//2
        self.angle = 0
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)

    def draw(self, ganhar):
        #ganhar.blit(self.img, [self.x, self.y, self.w, self.h])
        ganhar.blit(self.rotatedSurf, self.rotatedRect)

# rotaçoes da nave

    def paraEsquerda(self):
        self.angle += 5
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)

    def paraDireita(self):
        self.angle -= 5
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)

    def paraFrente(self):
        self.x += self.cosine * 6
        self.y -= self.sine * 6
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w // 2, self.y - self.sine * self.h // 2)

#Atualizar a localização da nave

    def attLocalizacao(self):
        if self.x > sw + 50:
            self.x = 0
        elif self.x < 0 - self.w:
            self.x = sw
        elif self.y < -50:
            self.y = sh
        elif self.y > sh + 50:
            self.y = 0

# Estrutura da Bala
class Bala(object):

    def __init__(self):
        self.point = player.head
        self.x, self.y = self.point
        self.w = 4
        self.h = 4
        self.c = player.cosine
        self.s = player.sine
        self.xv = self.c * 10
        self.yv = self.s * 10

    def move(self):
        self.x += self.xv
        self.y -= self.yv

    def draw(self, ganhar):
        pygame.draw.rect(ganhar, (255, 255, 255), [self.x, self.y, self.w, self.h])

# Quando a nave sair da tela ela retorna pelo outro lado 

    def checkOffScreen(self):
        if self.x < -50 or self.x > sw or self.y > sh or self.y < -50:
            return True

# Funções Asteroids
class Asteroid(object):
    def __init__(self, rank):
        self.rank = rank
        if self.rank == 1:
            self.image = asteroid50
        elif self.rank == 2:
            self.image = asteroid100
        else:
            self.image = asteroid150
        self.w = 50 * rank
        self.h = 50 * rank
        self.ranPoint = random.choice([(random.randrange(0, sw-self.w), random.choice([-1*self.h - 5, sh + 5])), (random.choice([-1*self.w - 5, sw + 5]), random.randrange(0, sh - self.h))])
        self.x, self.y = self.ranPoint
        if self.x < sw//2:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.y < sh//2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * random.randrange(1,3)
        self.yv = self.ydir * random.randrange(1,3)

    def draw(self, ganhar):
        ganhar.blit(self.image, (self.x, self.y))

# funções da estrela
class Estrela(object):
    def __init__(self):
        self.img = estrela
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.ranPoint = random.choice([(random.randrange(0, sw - self.w), random.choice([-1 * self.h - 5, sh + 5])),
                                       (random.choice([-1 * self.w - 5, sw + 5]), random.randrange(0, sh - self.h))])
        self.x, self.y = self.ranPoint
        if self.x < sw//2:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.y < sh//2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * 2
        self.yv = self.ydir * 2

    def draw(self, ganhar):
        ganhar.blit(self.img, (self.x, self.y))


def redrawGameWindow():
    ganhar.blit(bg, (0,0))
    font = pygame.font.SysFont('arial',30)
    vidasText = font.render('vidas: ' + str(vidas), 1, (255, 255, 255))
    playAgainText = font.render('Press Tab to Play Again', 1, (255,255,255))
    pontuacaoText = font.render('pontuacao: ' + str(pontuacao), 1, (255,255,255))
    maximapontuacaoText = font.render('maxima pontuacao: ' + str(maximapontuacao), 1, (255, 255, 255))

# Para cada bala dentro do playerBalas ele desenha uma nova bala

    player.draw(ganhar)
    for a in asteroids:
        a.draw(ganhar)
    for b in playerBalas:
        b.draw(ganhar)
    for s in estrelas:
        s.draw(ganhar)
   

    if rapidFire:
        pygame.draw.rect(ganhar, (0, 0, 0), [sw//2 - 51, 19, 102, 22])
        pygame.draw.rect(ganhar, (255, 255, 255), [sw//2 - 50, 20, 100 - 100*(count - rfStart)/500, 20])

    if fimdejogo:
        ganhar.blit(playAgainText, (sw//2-playAgainText.get_width()//2, sh//2 - playAgainText.get_height()//2))
    ganhar.blit(pontuacaoText, (sw- pontuacaoText.get_width() - 25, 25))
    ganhar.blit(vidasText, (25, 25))
    ganhar.blit(maximapontuacaoText, (sw - maximapontuacaoText.get_width() -25, 35 + pontuacaoText.get_height()))
    pygame.display.update()


player = Player()
playerBalas = []
asteroids = []
count = 0
estrelas = []

run = True

while run:
    
    timer.tick(60)
    count += 1
    if not fimdejogo:
        if count % 50 == 0:
            ran = random.choice([1,1,1,2,2,3])
            asteroids.append(Asteroid(ran))
        if count % 1000 == 0:
            estrelas.append(estrela())
        

# ao acertar o asteroid ele ganha uma pontuação 
            for b in playerBalas:
                if (b.x >= a.x and b.x <= a.x + a.w) or b.x + b.w >= a.x and b.x + b.w <= a.x + a.w:
                    if (b.y >= a.y and b.y <= a.y + a.h) or b.y + b.h >= a.y and b.y + b.h <= a.y + a.h:
                        
                    # tratar depois colocar para o led acender aqui
                        pontuacao += 50
                        break

       

        player.attLocalizacao()
        for b in playerBalas:
            b.move()
            if b.checkOffScreen():
                playerBalas.pop(playerBalas.index(b))


        for a in asteroids:
            a.x += a.xv
            a.y += a.yv

            if (a.x >= player.x - player.w//2 and a.x <= player.x + player.w//2) or (a.x + a.w <= player.x + player.w//2 and a.x + a.w >= player.x - player.w//2):
                if(a.y >= player.y - player.h//2 and a.y <= player.y + player.h//2) or (a.y  +a.h >= player.y - player.h//2 and a.y + a.h <= player.y + player.h//2):
                    vidas -= 1
                    asteroids.pop(asteroids.index(a))
                    
                    break

            # Bala colisao
            
            for b in playerBalas:
                if (b.x >= a.x and b.x <= a.x + a.w) or b.x + b.w >= a.x and b.x + b.w <= a.x + a.w:
                    if (b.y >= a.y and b.y <= a.y + a.h) or b.y + b.h >= a.y and b.y + b.h <= a.y + a.h:
                        if a.rank == 3:
                        
                            pontuacao += 10
                            na1 = Asteroid(2)
                            na2 = Asteroid(2)
                            na1.x = a.x
                            na2.x = a.x
                            na1.y = a.y
                            na2.y = a.y
                            asteroids.append(na1)
                            asteroids.append(na2)
                        elif a.rank == 2:
                            
                            pontuacao += 20
                            na1 = Asteroid(1)
                            na2 = Asteroid(1)
                            na1.x = a.x
                            na2.x = a.x
                            na1.y = a.y
                            na2.y = a.y
                            asteroids.append(na1)
                            asteroids.append(na2)
                        else:
                            pontuacao += 30
                            
                        asteroids.pop(asteroids.index(a))
                        playerBalas.pop(playerBalas.index(b))
                        break

        for s in estrelas:
            s.x += s.xv
            s.y += s.yv
            if s.x < -100 - s.w or s.x > sw + 100 or s.y > sh + 100 or s.y < -100 - s.h:
                estrelas.pop(estrelas.index(s))
                break
            for b in playerBalas:
                if (b.x >= s.x and b.x <= s.x + s.w) or b.x + b.w >= s.x and b.x + b.w <= s.x + s.w:
                    if (b.y >= s.y and b.y <= s.y + s.h) or b.y + b.h >= s.y and b.y + b.h <= s.y + s.h:
                        rapidFire = True
                        rfStart = count
                        estrelas.pop(estrelas.index(s))
                        playerBalas.pop(playerBalas.index(b))
                        break

        if vidas <= 0:
            fimdejogo = True

        if rfStart != -1:
            if count - rfStart > 500:
                rapidFire = False
                rfStart = -1

# controles do jogo

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.paraEsquerda()
        if keys[pygame.K_RIGHT]:
            player.paraDireita()
        if keys[pygame.K_UP]:
            player.paraFrente()
        if keys[pygame.K_SPACE]:
            if rapidFire:
                playerBalas.append(Bala())
                

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not fimdejogo:
                    if not rapidFire:
                        playerBalas.append(Bala())
                        
            if event.key == pygame.K_m:
                if isSoundOn:
                            shoot.play()
            if event.key == pygame.K_m:
                isSoundOn = not isSoundOn
            if event.key == pygame.K_TAB:
                if fimdejogo:
                    fimdejogo = False
                    vidas = 3
                    asteroids.clear()
                    estrelas.clear()
                    if pontuacao > maximapontuacao:
                        maximapontuacao = pontuacao
                    pontuacao = 0

    redrawGameWindow()
pygame.quit()