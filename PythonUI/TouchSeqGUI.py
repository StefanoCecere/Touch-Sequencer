#!/usr/bin/env python

#Import Modules
import os, pygame

from pygame.locals import *
from pygame.compat import geterror

pygame.init()


class MainMenu():
    def __init__(self):
        self.mainBG, self.mainBGrect = load_image('mainMenu.bmp')
        
        self.playingTracks = [0 for notes in range(10)]
        
        self.mainSurface = pygame.Surface((1024,600))
        self.mainSurface = self.mainSurface.convert()
        
        self.mainSurface.fill((250, 250, 250))

    def trackPress(self, pos):
        col = pos[0]
        row = pos[1]
        track = int(round(row / 60))
        mainObj.modeChange(2)
        

    def optionsPress(self, pos):
        row = pos[0]
        pos = pos[1]


    def drawScreen(self):
        self.mainSurface.blit(self.mainBG, (0,0))
        return self.mainSurface
        
    def mouseInput(self, pos):
        col = pos[0]
        row = pos[1]
        if col >= 600:
            self.optionsPress(pos)
        else:
            self.trackPress(pos)
            


class GridTrack():

    def __init__(self):
        self.button1, self.button1rect               = load_image('button1.bmp')
        self.button2, self.button1rect               = load_image('button2.bmp')
        self.navButton1, self.navButton1rect         = load_image('navButton1.bmp')
        self.navButton2, self.navButton2rect         = load_image('navButton2.bmp')
        self.navButtonWide1, self.navButtonWide1rect = load_image('navButtonWide1.bmp')
        self.navButtonWide2, self.navButtonWide2rect = load_image('navButtonWide2.bmp')
        self.optionsbg, self.optionsbgrect           = load_image('optionsBG.bmp')
        
        self.trackgrid   = [[0 for row in range(8)] for col in range(16)]
        self.patterngrid = [0 for col in range(8)]
        self.midinotes   = [0 for notes in range(8)]
        
        
        self.playing          = 0
        self.midiChannel      = 1
        self.midiVelocity     = 1
        self.patternSeqLength = 1
        self.patternNumber    = 0
        
        self.trackMode = 'grid'
        
        
        self.trackSurface = pygame.Surface((1024,600))
        self.trackSurface = self.trackSurface.convert()
        self.trackSurface.fill((250, 250, 250))

    
    # display functions
    
    def drawGrid(self):
        for col in range(16):
            for row in range(8):
                buttonval = self.trackgrid[col][row]
                if buttonval == 0:
                    self.trackSurface.blit(self.button1, ((col * 64),(row * 64)))
                elif buttonval == 1:
                    self.trackSurface.blit(self.button2, ((col * 64),(row * 64)))
                elif buttonval == 2:
                    self.trackSurface.blit(self.button3, ((col * 64),(row * 64)))
                elif buttonval == 3:
                    self.trackSurface.blit(self.button4, ((col * 64),(row * 64)))
                elif buttonval == 4:
                    self.trackSurface.blit(self.button5, ((col * 64),(row * 64)))


    def drawNavButtons(self):
        for col in range(12):
            if col < 8:
                if col == self.patternNumber:
                    self.trackSurface.blit(self.navButton1, ((col * 64),512))
                else:
                    self.trackSurface.blit(self.navButton2, ((col * 64),512))
            else:
                if col == self.patternNumber:
                    self.trackSurface.blit(self.navButtonWide1, ((((col - 8) * 128) + 512),512))
                else:
                    self.trackSurface.blit(self.navButtonWide2, ((((col - 8) * 128) + 512),512))


    def drawMidiOptions(self):
        self.trackSurface.blit(self.optionsbg, (512,0))
        for note in range(8):
            noteval = str(self.midinotes[note])
            font = pygame.font.Font(None, 32)
            notetext = font.render(noteval, 1, (255, 255, 255))
            textpos = (600,((note * 36) + 84))
            self.trackSurface.blit(notetext, textpos)
        
        noteval = str(self.midiChannel)
        font = pygame.font.Font(None, 32)
        notetext = font.render(noteval, 1, (255, 255, 255))
        textpos = (856,212)
        self.trackSurface.blit(notetext, textpos)
        
        noteval = str(self.midiVelocity)
        font = pygame.font.Font(None, 32)
        notetext = font.render(noteval, 1, (255, 255, 255))
        textpos = (856,84)
        self.trackSurface.blit(notetext, textpos)

    def drawPlayButton(self):
        buttonval = self.playing
        if buttonval == 0:
            self.trackSurface.blit(self.button1, (856,320))
        elif buttonval == 1:
            self.trackSurface.blit(self.button2, (856,320))

    def drawPatternSeq(self):
        for col in range(8):
            for row in range(8):
                if (self.patterngrid[col]) == row:
                    self.trackSurface.blit(self.button1, ((col * 64),(row * 64)))
                else:
                    self.trackSurface.blit(self.button2, ((col * 64),(row * 64)))

    def drawPatternSeqLength(self):
        for seqlength in range(8):
            seqlength += 1
            if seqlength <= self.patternSeqLength:
                xval = ((seqlength * 64) + (7 * 64))
                yval = (7 * 64)
                self.trackSurface.blit(self.button1, (xval,yval))
            else:
                xval = ((seqlength * 64) + (7 * 64))
                yval = (7 * 64)
                self.trackSurface.blit(self.button2, (xval,yval))


    def drawGridScreen(self):
        self.trackSurface.fill((250, 250, 250))
        self.drawGrid()
        self.drawNavButtons()

    def drawOptionsScreen(self):
        self.trackSurface.fill((250, 250, 250))
        self.drawPatternSeq()
        self.drawPatternSeqLength()
        self.drawMidiOptions()
        self.drawPlayButton()
        self.drawNavButtons()

        
    # functions that will be called from OSC messages
    
    def setSeqStep(self, step):
        self.trackgrid[col][row] = buttonval

    def updateGridButton(self, col, row):
        self.trackgrid[col][row] = self.trackgrid[col][row] + 1
        if self.trackgrid[col][row] > 1:
            self.trackgrid[col][row] = 0

    def updatePatternSeq(self, col, row):
        self.patterngrid[col] = row
        

    def clearGrid(self):
        for col in range(16):
            for row in range(8):
                self.trackgrid[col][row] = 0


    # mouse input functions

    def mouseInput(self, pos):
        if self.trackMode == 'grid':
            self.inputGridScreen(pos)
        elif self.trackMode == 'options':
            self.inputOptionsScreen(pos)


    def inputGridScreen(self, pos):
        col = int(round(pos[0] / 64))
        row = int(round(pos[1] / 64))
        
        if row < 8:
            self.updateGridButton(col, row)
        else:
            self.navButtonInterface(col)

    
    def navButtonInterface(self, col):
        if col < 8:
            self.patternNumber = col
            self.trackMode = 'grid'
        elif col == 8 or col == 9:
            self.patternNumber = 8
            self.trackMode = 'options'
        elif col == 10 or col == 11:
            blah = 1
        elif col == 12 or col == 13:
            blah = 1
        elif col == 14 or col == 15:
            self.patternNumber = 1
            self.trackMode = 'grid'
            mainObj.modeChange(1)
        
    
    def inputOptionsScreen(self, pos):
        col = pos[0]
        row = pos[1]
        col = int(round(col / 64))
        row = int(round(row / 64))
        if row < 8 and col < 8:
            self.updatePatternSeq(col,row)
        else:
            self.navButtonInterface(col)

    def drawScreen(self):
        if self.trackMode == 'options':
            self.drawOptionsScreen()
        elif self.trackMode == 'grid':
            self.drawGridScreen()
        return self.trackSurface





#functions to create our resources
def load_image(name, colorkey=None):

    main_dir = os.path.split(os.path.abspath(__file__))[0]
    data_dir = os.path.join(main_dir, 'gfx')

    fullname = os.path.join(data_dir, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error:
        print ('Cannot load image:', fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()




class Globject():

    def __init__(self):
        self.screen = pygame.display.set_mode((1024, 600))
        background = pygame.Surface(self.screen.get_size())
        self.background = background.convert()
        
        self.mode = 1
        
        self.grid = GridTrack()
        self.menu = MainMenu()
        self.modeObject = self.menu

    def drawStuff(self):
        screenImage = self.modeObject.drawScreen()
        self.background.blit(screenImage, (0,0))
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

    def modeChange(self, mode):
        if mode != self.mode:
            self.mode = mode
            if mode == 1:
                self.modeObject = self.menu
                print "mode change"
            elif mode == 2:
                self.modeObject = self.grid
                print "mode change"

def main():


    global mainObj

    mainObj = Globject()
    
    clock = pygame.time.Clock()

    loop = True
    while loop:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                loop = False
            if event.type == pygame.MOUSEBUTTONDOWN :
                mouseClick = pygame.mouse.get_pos()
                mainObj.modeObject.mouseInput(mouseClick)
        
        mainObj.drawStuff()


    pygame.quit()



if __name__ == '__main__':
    main()
