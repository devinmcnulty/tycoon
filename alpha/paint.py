import pygame, sys, os
from pygame.locals import *

# Display variables
FPS = 120

MENUHEIGHT = 50
DRAWHEIGHT = 600
DRAWWIDTH = 600

WINDOWHEIGHT = MENUHEIGHT + DRAWHEIGHT
WINDOWWIDTH = DRAWWIDTH
CELLSIZE = 50





assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be multiple of cell size"
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be multiple of cell size"
assert MENUHEIGHT % CELLSIZE == 0, "Menu height must be multiple of cell size"

# Color variables

RED = (255, 0, 0)
ORANGERED = (226, 87, 30)
ORANGE = (255, 127, 0) 
YELLOW = (255, 255, 0) 
GREEN = (0, 255, 0)
GREENBLUE =  (150, 191, 51)
BLUE = (0, 0, 255)
INDIGO = (75, 0, 130)
VIOLET = (139, 0, 255)
WHITE = (255, 255, 255)
BROWN = (139,69,19)
BLACK = (0, 0, 0)
GRAY = (211,211,211)
COLORS = [ RED, ORANGERED, ORANGE, YELLOW, GREEN, GREENBLUE, BLUE, INDIGO, VIOLET, WHITE, BROWN, BLACK ]

# Pen variables
PEN = BLACK

# Background variables
BGCELLSIZE = int(CELLSIZE/5)
BGCOLORS = [WHITE, GRAY]

class Cell(pygame.Rect):
    
    def __init__(self, topleft):
        pygame.Rect.__init__(self,0 ,0 , CELLSIZE, CELLSIZE)
        self.topleft = topleft
        
    def draw(self):
        pygame.draw.rect(DISPLAY, self.color, self)
        
class DrawCell(Cell):
    
    def __init__(self, topleft):
        Cell.__init__(self, topleft)
        self.color = WHITE
        self.view = False
        
    def isClicked(self, mouse):
        global PEN
        if (self.left < mouse[0] < self.right) and (self.top < mouse[1] - MENUHEIGHT < self.bottom):
            self.view = True
            self.color = PEN
            
        
class PickerCell(Cell):
    
    def __init__(self, topleft, color):
        Cell.__init__(self, topleft)
        self.color = color
        self.view = True

    
    def isClicked(self, mouse):
        global PEN
        if (self.left < mouse[0] < self.right) and (self.top < mouse[1] < self.bottom):
            PEN = self.color
            
class Background(pygame.Surface):
    
    def __init__(self):
        pygame.Surface.__init__(self, (DRAWWIDTH, DRAWHEIGHT))
        for i in range(0, int(DRAWWIDTH/BGCELLSIZE)):
            for j in range(0, int(DRAWHEIGHT/BGCELLSIZE)):
                smallcell = pygame.Rect((i*BGCELLSIZE),(j*BGCELLSIZE),BGCELLSIZE, BGCELLSIZE)
                color = BGCOLORS[(i+j)%2]
                pygame.draw.rect(self, color, smallcell)
        

def populateCells(cells, group):
    if group == "picker":
        for i in range(0, int(DRAWWIDTH/CELLSIZE)):
            cells.append(PickerCell((i*CELLSIZE,0), COLORS[i]))
    elif group == "draw":
        for i in range(0, int(DRAWWIDTH/CELLSIZE)):
            for j in range(0, int(WINDOWHEIGHT/CELLSIZE)):
                cells.append(DrawCell((i*CELLSIZE,j*CELLSIZE)))

def main():
    
    global CENTER, BASICFONT, DISPLAY, FPSCLOCK, PAINTAREA, PAINTEXPORT
    
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAY = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    PAINTAREA = pygame.Surface((DRAWWIDTH, DRAWHEIGHT))
    PAINTEXPORT = pygame.Surface((DRAWWIDTH, DRAWHEIGHT), pygame.SRCALPHA, 32)
    PAINTEXPORT = PAINTEXPORT.convert_alpha()
    CENTER = (DISPLAY.get_rect().centerx, DISPLAY.get_rect().centery) 
    BASICFONT = pygame.font.SysFont("Arial", 30)
    pygame.display.set_caption("Paint")
    
    showStartScreen()
    
    while True:
        runGame()
        showEndScreen()
        
def runGame():
    # Initialize background
    BACKGROUND = Background()
    
    # Initialize cells
    pickerCells = []
    drawCells = []
    allCells = [pickerCells, drawCells]
    populateCells(pickerCells, "picker")
    populateCells(drawCells, "draw")
    while True: 
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            
            if event.type == MOUSEBUTTONDOWN:
                for cells in allCells:
                    for cell in cells:
                        cell.isClicked(event.pos)
            
            if event.type == KEYDOWN:
                if event.key == K_RETURN or event.key == K_s:
                    for cell in drawCells:
                        if cell.view == True:
                            pygame.draw.rect(PAINTEXPORT, cell.color, cell)
                    pygame.image.save(PAINTEXPORT, os.path.join(os.path.dirname(__file__), "product.png"))

        PAINTAREA.blit(BACKGROUND, (0,0))
        
        for cell in pickerCells:
            cell.draw()
        for cell in drawCells:
            if cell.view == True:
                pygame.draw.rect(PAINTAREA, cell.color, cell)
                
        DISPLAY.blit(PAINTAREA, (0, MENUHEIGHT))

        pygame.display.update()
        FPSCLOCK.tick(FPS)
        
def showStartScreen():
    
    
    DISPLAY.fill(WHITE)
    titletext = BASICFONT.render("Draw your product!", True, BLACK)
    titletextrect = titletext.get_rect()
    titletextrect.center = CENTER
    DISPLAY.blit(titletext, titletextrect)
    pygame.display.update()
    
    while True:
        
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:    
                return

def showEndScreen():
    return
                
def terminate():
    pygame.quit()
    sys.exit()
    
main()