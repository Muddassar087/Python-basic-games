# @author Muhammad Muddassar 2021
# code sample for reinforcement learning practices

import random
import sys, time
import pygame
from constants import *

# An individual block represnt single rectangle in snake body which has certain perameters like its x,y postions and width
# height with prevx and prevy which stores prevoius postions
class block:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.prevX = x
        self.prevY = y
        self.width = width
        self.height = height
        self.color = color

    def setxy(self, x, y):
        self.x = x
        self.y = y

    # this methods updates the block with given direction and speed
    def updatepos(self, direction, speed):

        if direction is 'r': self.x += speed
        if direction is 'l': self.x -= speed
        if direction is 'u': self.y -= speed
        if direction is 'd': self.y += speed

    # draw method creats the rectangle this should be rerendered each time postion changes and also update the prev values
    def draw(self):
        pygame.draw.rect(screen, self.color, [self.x, self.y, self.width, self.height])
        self.prevX = self.x
        self.prevY = self.y

class Snake:
    length = 3
    body = []
    head = block(WIDTH/2, HEIGHT/2, 20,20, GREEN) # single head starting from the mid of screen

    # this method creats snake body each time snake eat food this method should be called and update the body
    def makeSnakeBody(self):
        if self.body.__len__() <= 0:
            self.body.append(self.head)
            for i in range(self.length-1):
                tail = self.body[-1]
                self.body.append(block(tail.prevX, tail.prevY, 20,20, WHITE))

        elif self.length > self.body.__len__():
            # get tail and add a new block on the previous position of tail
            tail = self.body[-1]
            self.body.append(block(tail.prevX, tail.prevY, 20,20, WHITE))

    def drawSnake(self):
        for b in self.body:
            b.draw()

    # move the snake with respect to its head
    def moveSnake(self, direction, vel):
        self.head = self.body[0]
        self.head.updatepos(direction, vel)
        # get the reference of head which then updates to the curent block in the loop
        tail = self.head
        for i in range(1,len(self.body)):
            self.body[i].setxy(tail.prevX, tail.prevY)
            tail = self.body[i] # update the tails with current block

        # handke the boundries
        if self.head.x > WIDTH: self.head.x = 5
        elif self.head.x < 0: self.head.x = WIDTH - 5
        elif self.head.y < 0: self.head.y = HEIGHT - 5
        elif self.head.y > HEIGHT: self.head.y = 5

# check if the food and snake head has been collided then update the food pos and snake length
def collidionDetection(head, food):
    if (head.x >= food.x) and (head.x <= food.x + 20) or (head.x + 20 >= food.x) and (head.x + 20 <= food.x + 20):
        if (head.y >= food.y) and (head.y <= food.y + 20) or (head.y + 20 >= food.y) and (head.y + 20 <= food.y + 20):
            food.setxy(random.randrange(20, WIDTH-20), random.randrange(20,HEIGHT-20))
            food.draw()
            snake.length+=1
            snake.makeSnakeBody()

    if snake.length > 5:
        for b in snake.body[1:]:
            if head.x == b.x and head.y == b.y:
                snake.length = 3
                snake.body = []
                snake.makeSnakeBody()
                main()

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake AI")
clock = pygame.time.Clock()

snake = Snake( )
snake.makeSnakeBody()

myfont = pygame.font.SysFont(pygame.font.get_default_font(), 25, bold=False, italic=False)
food = block(80, 100, 20, 20, RED)

def main():
        
    running = True
    direction = 'r'

    while running:
        clock.tick(25)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: direction = 'l'
                elif event.key == pygame.K_RIGHT: direction = 'r'
                elif event.key == pygame.K_UP: direction = 'u'
                elif event.key == pygame.K_DOWN: direction = 'd'

        screen.fill(BGCOLOR)

        snake.drawSnake()
        snake.moveSnake(direction, 20)
        food.draw()
        collidionDetection(snake.head, food)

        text = myfont.render("Length - {0}".format(snake.length),False, (255, 255, 255))
        text2 = myfont.render("Generation - {0}".format(0),False, (255, 255, 255))
        screen.blit(text, (10,10))
        screen.blit(text2, (WIDTH-150,10))
        
        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()