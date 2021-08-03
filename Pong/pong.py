import pygame
import sys
from constants import *

class Player:
    def __init__(self, x, y, width, height) -> None:
        self.hit = 0
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self):
        pygame.draw.rect(screen, WHITE, [self.x, self.y, self.width, self.height])

    def update(self, direction, vel):
        if direction is 'u' and self.y >= 20: self.y -= vel
        elif direction is 'd' and self.y <= HEIGHT-120: self.y += vel

class Ball:
    def __init__(self) -> None:
        self.x = int(WIDTH/2)
        self.y = int(HEIGHT/2)

        self.xvel = 10
        self.yvel = -10
    
    def draw(self):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), 10)

    def update(self, player1, player2):
        # always oppose the current direction by changing the direciton 10, -10
        if self.x > WIDTH - 10:
            self.xvel = -10
            player1.hit += 1
        if self.x < 10:
            self.xvel = 10
            player2.hit += 1
        if self.y >= HEIGHT - 10:
            self.xvel = int(self.xvel/10) * 10 # if xvel is negetive then it will remain negative -10/10 = -1 * 10 = -10
            self.yvel = -10
        if self.y <= 10:
            self.xvel = int(self.xvel/10) * 10 
            self.yvel = 10 
        
        self.x += self.xvel; # add the direction to the postion
        self.y += self.yvel;
        
def line():
    pygame.draw.line(screen, GRAY, [WIDTH/2, 0], [WIDTH/2, HEIGHT], 1)

def collisionWithPlayer(player, player2, ball):
    if (ball.x == player.x + player.width) and (ball.y > player.y) and (ball.y < player.y+100):
        ball.xvel = -1 * ball.xvel

    if (ball.x+10 == player2.x) and (ball.y + 10 >= player2.y) and (ball.y + 10 <= player2.y+100):
        ball.xvel = -1 * ball.xvel

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake AI")
clock = pygame.time.Clock()
myfont = pygame.font.SysFont(pygame.font.get_default_font(), 40, bold=False, italic=False)

player1 = Player(10, 50, 30, 100)
player2 = Player(WIDTH-40, 200, 30, 100)
ball = Ball()

def main():
    running = True
    while running:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            player1.update(direction="u", vel=10)
        elif keys[pygame.K_DOWN]:
            player1.update(direction="d", vel=10)

        if keys[pygame.K_w]:
            player2.update(direction="u", vel=10)
        elif keys[pygame.K_s]:
            player2.update(direction="d", vel=10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
           
        screen.fill(BGCOLOR)
        
        # rendering the text here
        text = myfont.render("{0}".format(player1.hit), False, GREEN)
        text2 = myfont.render("{0}".format(player2.hit), False, GREEN)
        screen.blit(text, (10,10))
        screen.blit(text2, (WIDTH-40,10))

        line()
        player1.draw()
        player2.draw()
        ball.update(player1,player2)
        ball.draw()
        collisionWithPlayer(player1, player2, ball)
        
        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()