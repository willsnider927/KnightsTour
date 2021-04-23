import sys
import math
import time

try:
    import pygame
except ImportError:
    import pip
    pip.main(['install','--user','pygame'])
    import pygame

def pathshow(m,n,path):
    pygame.init()
    white = (255,255,255)
    grey = (200, 200, 200)
    black = (0,0,0,)
    blue = (0,0,240)
    green = (0,240,0)
    squareSize = 30
    screen = pygame.display.set_mode((squareSize*n+10,squareSize*m+10))
    pygame.display.set_caption("Don't press close button ->")
    screen.fill(blue)
    knight = pygame.image.load('knighttran.png')
    num = 0
    check = 1
    letters = pygame.font.SysFont("Times New Roman", 28)
    letters2 = pygame.font.SysFont("Times New Roman", 18)
    #make board
    if n % 2 == 1: #if area is odd
        for i in range(m):
            pygame.event.get()
            for j in range(n):
                if check == 1:
                    pygame.draw.rect(screen, white, [squareSize*j + 5,squareSize*i + 5,squareSize,squareSize])
                else:
                    pygame.draw.rect(screen, grey, [squareSize*j + 5,squareSize*i + 5,squareSize,squareSize])
                num = num + 1
                check = not check
    else:
        for i in range(m):
            pygame.event.get()
            for j in range(n):
                if check == 1:
                    pygame.draw.rect(screen, white, [squareSize*j + 5,squareSize*i + 5,squareSize,squareSize])
                else:
                    pygame.draw.rect(screen, grey, [squareSize*j + 5,squareSize*i + 5,squareSize,squareSize])
                num = num + 1
                check = not check
            check = not check
    pygame.display.update()
    #do path
    newpath = []
    for i in range(len(path)):
        pygame.event.get()
        row = int(path[i] % n)
        col = int(math.floor(path[i] / n))
        newpath.append([row,col])
        screen.blit(knight, (squareSize*row + 5,squareSize*col + 5))
        pygame.display.update()
        time.sleep(.2)
        prevrow = row
        prevcol = col
        pygame.draw.rect(screen, white, [squareSize*row + 5,squareSize*col + 5,squareSize,squareSize])
        pygame.draw.rect(screen, green, [squareSize*row + 6,squareSize*col + 6,squareSize-2,squareSize-2])
        if i < 10: 
            screen.blit(letters.render(str(i), 1, black), (squareSize*row + 13,squareSize*col + 4))
            screen.blit(letters.render(str(i), 1, black), (squareSize*prevrow + 13,squareSize*prevcol + 4))
        elif i < 100:
            screen.blit(letters.render(str(i), 1, black), (squareSize*row + 6,squareSize*col + 4))
            screen.blit(letters.render(str(i), 1, black), (squareSize*prevrow + 6,squareSize*prevcol + 4))
        else:
            screen.blit(letters2.render(str(i), 1, black), (squareSize*row + 6,squareSize*col + 8))
            screen.blit(letters2.render(str(i), 1, black), (squareSize*prevrow + 6,squareSize*prevcol + 8))
        #pygame.draw.line(screen, grey, (squareSize*prevrow+15,squareSize*prevcol+15), (squareSize*row + 15,squareSize*col + 15), 2)
    pygame.display.update()
    end=str(input("When you are done with the path, press enter on this command line to exit.\n"))
    pygame.quit()

#order back to front: green, line, num


#pathshow(17,9,[0,1,2,3,4,5,6,7,35])
#screen.blit(knight, (squareSize*j + 5,squareSize*i + 5))
#screen.blit(letters.render(str(num), 1, black), (squareSize*j + 5,squareSize*i + 5))