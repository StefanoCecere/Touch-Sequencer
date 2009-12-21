#!/usr/bin/env python

#Import Modules
import os, pygame, osc

from pygame.locals import *
from pygame.compat import geterror
    
class MainMenu():
    def __init__(self):
        self.mainBG, self.mainBGrect = load_image('mainMenu.bmp','backgrounds')
        self.gobutton, self.gobuttonrect = load_image('gobutton.bmp','buttons')
        self.stopbutton, self.stopbuttonrect = load_image('stopbutton.bmp','buttons')
        
        self.playingTracks = [0 for notes in range(10)]
        self.bpm = 140
        self.globalplay = 0
        self.trackNo = 0
        
        self.mainSurface = pygame.Surface((1024,600))
        self.mainSurface = self.mainSurface.convert()
        
        self.mainSurface.fill((250, 250, 250))

    def trackPress(self, pos):
        xval = pos[0]
        yval = pos[1]
        
        track = int(round(yval / 60))
        self.trackNo = track
        sendOSCMessage('/grid/track_select', [track + 1])
        if 444 < xval < 544:
            if self.playingTracks[track] == 0:
                self.playingTracks[track] = 1
            else:
                self.playingTracks[track] = 0
            sendOSCMessage('/grid/track/control/play', [self.playingTracks[track]])
        else:
            sendOSCMessage('/grid/track/get/pattern_grid', [0])
            mainObj.modeChange(2)

    def changeBpm(self, value):
        bpm = self.bpm + value
        if bpm < 80:
            bpm = 80
        elif bpm > 300:
            bpm = 300
        self.bpm = bpm
        sendOSCMessage('/bpm', [self.bpm])

    def optionsPress(self, pos):
        xval = int(round(pos[0] / 32))
        yval = int(round(pos[1] / 32))
        
        bpmRect = ((20,2),(31,11))
        playRect = ((22,14),(29,17))
        
        if 18 < xval < 31 and 1 < yval < 11:
        
            if yval < 4:
                xval = (xval - 18)
                if xval < 5:
                    self.changeBpm(100)
                elif xval > 8:
                    self.changeBpm(10)
                else:
                    self.changeBpm(10)
            elif yval > 8:
                xval = (xval - 18)
                if xval < 5:
                    self.changeBpm(-100)
                elif xval > 8:
                    self.changeBpm(-10)
                else:
                    self.changeBpm(-1)
                
        elif 20 < xval < 29 and 13 < yval < 17:
            if self.globalplay == 0:
                self.globalplay = 1
            else:
                self.globalplay = 0
            sendOSCMessage('/global_play', [self.globalplay])

    def drawMainScreen(self):
        self.mainSurface.blit(self.mainBG, (0,0))
        bpm = str(self.bpm)
        font = pygame.font.Font(None, 256)
        bpmtext = font.render(bpm, 1, (255, 255, 255))
        textpos = ((20 * 32),(4 * 32))
        self.mainSurface.blit(bpmtext, textpos)
        for tracks in range(10):
            pos = (444, ((tracks *60) + 5))
            if self.playingTracks[tracks] == 1:
                self.mainSurface.blit(self.gobutton, pos)
            else:
                self.mainSurface.blit(self.stopbutton, pos)
    

    def drawScreen(self):
        self.drawMainScreen()
        return self.mainSurface

    def mouseInput(self, pos):
        col = pos[0]
        row = pos[1]
        if col >= 576:
            self.optionsPress(pos)
        else:
            self.trackPress(pos)


class GridTrack():

    def __init__(self):
        self.button1, self.button1rect               = load_image('button1.bmp','buttons')
        self.button2, self.button1rect               = load_image('button2.bmp','buttons')
        self.navButton1, self.navButton1rect         = load_image('navButton1.bmp','buttons')
        self.navButton2, self.navButton2rect         = load_image('navButton2.bmp','buttons')
        self.navButtonWide1, self.navButtonWide1rect = load_image('navButtonWide1.bmp','buttons')
        self.navButtonWide2, self.navButtonWide2rect = load_image('navButtonWide2.bmp','buttons')
        self.optionsbg, self.optionsbgrect           = load_image('optionsBG.bmp','backgrounds')
        
        self.trackgrid   = [[0 for row in range(8)] for col in range(16)]
        self.patterngrid = [0 for col in range(8)]
        self.midinotes   = [0 for notes in range(8)]
        
        self.updateValue      = ''
        
        self.gridpattern      = 0

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
            font = pygame.font.Font(None, 52)
            notetext = font.render(noteval, 1, (255, 255, 255))
            textpos = (600,((note * 40) + 64 + 4))
            self.trackSurface.blit(notetext, textpos)
        
        noteval = str(self.midiChannel)
        font = pygame.font.Font(None, 96)
        notetext = font.render(noteval, 1, (255, 255, 255))
        textpos = ((832 + 4),(192 + 4))
        self.trackSurface.blit(notetext, textpos)
        
        noteval = str(self.midiVelocity)
        font = pygame.font.Font(None, 96)
        notetext = font.render(noteval, 1, (255, 255, 255))
        textpos = ((832 + 4),(64 + 4))
        self.trackSurface.blit(notetext, textpos)

    def drawPatternSeq(self):
        for col in range(8):
            for row in range(8):
                if (self.patterngrid[col]) == row:
                    self.trackSurface.blit(self.button1, ((col * 64),(row * 64)))
                else:
                    self.trackSurface.blit(self.button2, ((col * 64),(row * 64)))

    def drawPlayButton(self):
        buttonval = mainObj.menu.playingTracks[mainObj.menu.trackNo]
        if buttonval == 0:
            self.trackSurface.blit(self.navButton1, (832,320))
        elif buttonval == 1:
            self.trackSurface.blit(self.navButton2, (832,320))

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
        self.drawNavButtons()
        self.drawPlayButton()

        
    # functions that will be called from OSC messages
    
    def setSeqStep(self, step):
        self.trackgrid[col][row] = buttonval

    def updateGridButton(self, col, row):
        self.trackgrid[col][row] = self.trackgrid[col][row] + 1
        if self.trackgrid[col][row] > 1:
            self.trackgrid[col][row] = 0
        data = [row + 1, col + 1, self.trackgrid[col][row]]
        sendOSCMessage('/grid/track/edit/pattern_grid', data)

    def updatePatternSeq(self, col, row):
        self.patterngrid[col] = row
        data = [col, (7 - row)]
        sendOSCMessage('/grid/track/edit/pattern_seq', data)

    def updatePatternSeqLength(self, col):
        self.patternSeqLength = (col - 7)
        sendOSCMessage('/grid/track/edit/pattern_seq_length', [self.patternSeqLength])

    def editPatternSeq(self, *msg):
        xval = msg[0][2]
        yval = 7 - msg[0][3]
        self.patterngrid[xval] = yval

    def editPatternSeqLength(self, *msg):
        length = msg[0][2]
        self.patternSeqLength = length

    def editGrid(self, *msg):
        yval = (msg[0][2] - 1)
        xval = (msg[0][3] - 1)
        dval = msg[0][4]
        self.trackgrid[xval][yval] = dval

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
            sendOSCMessage('/grid/track/get/pattern_grid', [col])
            sendOSCMessage('/grid/track/edit/pattern_number', [col])
            self.gridpattern = col
            self.patternNumber = col
            self.trackMode = 'grid'
        elif col == 8 or col == 9:
            self.patternNumber = 8
            self.trackMode = 'options'
            sendOSCMessage('/grid/track/get/pattern_seq',["bang"])
            sendOSCMessage('/grid/track/get/pattern_seq_length',["bang"])
        elif col == 10 or col == 11:
            blah = 1
        elif col == 12 or col == 13:
            blah = 1
        elif col == 14 or col == 15:
            self.patternNumber = 0
            self.trackMode = 'grid'
            mainObj.modeChange(1)

    def inputMidiOptions(self, pos):
        xval = pos[0]
        yval = pos[1]
        col = int(round(xval / 64))
        row = int(round(yval / 64))
        if 8 < col < 11 and 0 < row < 6:
            note = ((yval - 64) / 40)
            print "midi note", note
        elif 12 < col < 15 and row == 1:
            print "velocity"
        elif 12 < col < 15 and row == 3:
            print "channel"
        elif 12 < col < 15 and row == 5:
            playval = mainObj.menu.playingTracks[mainObj.menu.trackNo]
            if playval == 0:
                mainObj.menu.playingTracks[mainObj.menu.trackNo] = 1
                sendOSCMessage('/grid/track/control/play', 1)
            if playval == 1:
                mainObj.menu.playingTracks[mainObj.menu.trackNo] = 0
                sendOSCMessage('/grid/track/control/play', 0)
    
    def inputOptionsScreen(self, pos):
        col = pos[0]
        row = pos[1]
        col = int(round(col / 64))
        row = int(round(row / 64))
        if row > 7:
            self.navButtonInterface(col)
        elif col < 8:
            self.updatePatternSeq(col,row)
        elif row == 7:
            self.updatePatternSeqLength(col)
        else:
            self.inputMidiOptions(pos)

    def drawScreen(self):
        if self.trackMode == 'options':
            self.drawOptionsScreen()
        elif self.trackMode == 'grid':
            self.drawGridScreen()
        return self.trackSurface





#functions to create our resources
def load_image(name, subdir, colorkey=None):

    main_dir = os.path.split(os.path.abspath(__file__))[0]
    data_dir = os.path.join(main_dir, 'gfx')
    data_dir = os.path.join(data_dir, subdir)

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


def sendOSCMessage(address, value):

    print address, value

#    osc.sendMsg(address, value, '192.168.2.3', 9002)
    osc.sendMsg(address, value, '127.0.0.1', 9002)


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
            elif mode == 2:
                self.modeObject = self.grid


def printStuff(*msg):
    """deals with "print" tagged OSC addresses """

    print "printing in the printStuff function ", msg
    print "the oscaddress is ", msg[0][0]
    print "the value is ", msg[0][2]
    print "the value is ", msg[0][3]




def main():


    global mainObj

    pygame.init()

    osc.init()
    osc.listen('127.0.0.1', 9001)

    mainObj = Globject()
    
    clock = pygame.time.Clock()

    osc.bind(mainObj.grid.editGrid, "/grid/pattern_grid/edit")
    
    osc.bind(mainObj.grid.editPatternSeqLength, "/grid/pattern_seq/length")
    osc.bind(mainObj.grid.editPatternSeq, "/grid/pattern_seq")
    
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


    osc.dontListen()
    pygame.quit()



if __name__ == '__main__':
    main()
