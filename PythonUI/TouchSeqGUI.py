#!/usr/bin/env python

#Import Modules
import os, pygame, osc

from grid16 import *
from grid32 import *
from curve import *

import socket

from pygame.locals import *
#from pygame.compat import geterror
    
class MainMenu():

    def __init__(self):
        self.mainBG, self.mainBGrect            = load_image('mainMenu.png','backgrounds')
        self.gobutton, self.gobuttonrect        = load_image('gobutton.png','buttons')
        self.stopbutton, self.stopbuttonrect    = load_image('stopbutton.png','buttons')
        self.mainPlay, self.mainPlayrect        = load_image('mainPlay.png','buttons')
        self.mainStop, self.mainStoprect        = load_image('mainStop.png','buttons')
        
        self.playingTracks = [0 for notes in range(10)]
        self.trackTypes    = ['' for tracks in range(10)]
        self.bpm           = 140
        self.globalplay    = 0
        self.trackNo       = 0
        self.stepNumber    = 0
        self.connected     = 0
        
        self.mainSurface = pygame.Surface((1024,600))
        self.mainSurface = self.mainSurface.convert()
        
        self.mainSurface.fill((250, 250, 250))

    def trackPress(self, pos):
        xval = pos[0]
        yval = pos[1]
        
        track = int(round(yval / 60))
        self.trackNo = track
        
        sendOSCMessage('/grid/track_select', [track + 1])
        
        if 471 < xval < 571:
            if self.playingTracks[track] == 0:
                self.playingTracks[track] = 1
            else:
                self.playingTracks[track] = 0
            sendOSCMessage('/grid/track/control/play', [self.playingTracks[track]])
        else:
            mainObj.modeChange(self.trackTypes[track])
            

    def seqStepNumber(self, *msg):
        stepNum  = msg[0][2]
        self.stepNumber = stepNum

    def trackInfo(self, *msg):
        trackNum  = (msg[0][2] - 1)
        trackType = msg[0][3]
        self.trackTypes[trackNum] = trackType
        self.connected = 1
        print trackNum, trackType
        

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
        
        bpmRect     = ((20,2),(31,11))
        connectRect = ((22,12),(29,13))
        playRect    = ((22,15),(29,17))
        
        if 18 < xval < 31 and 1 < yval < 11:
        
            if yval < 4:
                if 18 < xval < 23:
                    self.changeBpm(100)
                elif 22 < xval < 27:
                    self.changeBpm(10)
                elif 27 < xval < 31:
                    self.changeBpm(1)
            elif yval > 8:
                if 18 < xval < 23:
                    self.changeBpm(-100)
                elif 22 < xval < 27:
                    self.changeBpm(-10)
                elif 27 < xval < 31:
                    self.changeBpm(-1)
                
        elif 20 < xval < 29 and 14 < yval < 18:
            if self.globalplay == 0:
                self.globalplay = 1
            else:
                self.globalplay = 0
            sendOSCMessage('/global_play', [self.globalplay])
        
        elif 20 < xval < 29 and 11 < yval < 15:
            if self.connected == 0:
                print "connected"
                sendOSCMessage('/track_info', ['bang'])

    def drawMainScreen(self):
        self.mainSurface.blit(self.mainBG, (0,0))
        
        if self.bpm < 100:
            bpm = ' ' + str(self.bpm)
        else:
            bpm = str(self.bpm)
        font = pygame.font.Font(pygame.font.match_font('arial') , 196)
        bpmtext = font.render(bpm, 1, (255, 255, 255))
        textpos = ((20 * 32),(3 * 32))
        self.mainSurface.blit(bpmtext, textpos)
        
        for tracks in range(10):
            pos = (471, ((tracks *60) + 5))
            if self.playingTracks[tracks] == 1:
                self.mainSurface.blit(self.gobutton, pos)
            else:
                self.mainSurface.blit(self.stopbutton, pos)
                
            trackType = str(self.trackTypes[tracks])
            font = pygame.font.Font(pygame.font.match_font('arial'), 45)
            displaytext = font.render(trackType, 1, (0, 0, 0))
            textpos = (16,(tracks * 60))
            self.mainSurface.blit(displaytext, textpos)
        
        if self.globalplay == 1:
            self.mainSurface.blit(self.mainPlay, (672, 480))
        else:
            self.mainSurface.blit(self.mainStop, (672, 480))
        
        if self.connected == 1:
            self.mainSurface.blit(self.mainPlay, (672, 384))
        else:
            self.mainSurface.blit(self.mainStop, (672, 384))



    def drawScreen(self):
        self.drawMainScreen()
        return self.mainSurface

    def mouseInput(self, type, pos):
        if type == 'down':
            col = pos[0]
            row = pos[1]
            if col >= 576:
                self.optionsPress(pos)
            else:
                self.trackPress(pos)




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

    global sendIP
    global sendPort

    osc.sendMsg(address, value, sendIP, sendPort)


class Globject():

    def __init__(self):
        self.screen = pygame.display.set_mode((1024, 600))
        background = pygame.Surface(self.screen.get_size())
        self.background = background.convert()
        
        self.mode = 'main'
        
        self.curve      = CurveTrack()
        self.grid16     = Grid16Track()
        self.grid32     = Grid32Track()
        self.menu       = MainMenu()
        self.modeObject = self.menu

    def drawStuff(self):
        screenImage = self.modeObject.drawScreen()
        self.background.blit(screenImage, (0,0))
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

    def modeChange(self, mode):
        if mode != self.mode:
            self.mode = mode
            if mode == 'main':
                self.modeObject = self.menu
            elif mode == 'grid16':
                self.modeObject = self.grid16
                self.modeObject.trackSetup()
            elif mode == 'grid32':
                self.modeObject = self.grid32
                self.modeObject.trackSetup()
            elif mode == 'curve':
                self.modeObject = self.curve
                self.modeObject.trackSetup()



def printStuff(*msg):

    print 'printing in the printStuff function ', msg
    print 'the oscaddress is ', msg[0][0]
    print 'the value is ', msg[0][2]




def main():


    global mainObj
    
    global sendIP
    global sendPort
    
    configFile = open('OSCadr.cfg', 'r')
    for line in configFile:
        line = line.split()
        if line[0] == "sendPort":
            sendPort = int(line[1])
        if line[0] == "sendIP":
            sendIP = line[1]
        if line[0] == "listenIP":
            listenIP = line[1]
        if line[0] == "listenPort":
            listenPort = int(line[1])

    pygame.init()

    osc.init()
    osc.listen(listenIP, listenPort)

    mainObj = Globject()
    
    clock = pygame.time.Clock()
    
    osc.bind(mainObj.curve.editCurve, '/curve/gui_curve/edit') 
    osc.bind(mainObj.curve.editMidi, '/curve/midi_params')
    osc.bind(mainObj.curve.editLengths, '/curve/curve_lengths')
    osc.bind(mainObj.curve.editPlayStates, '/curve/play_states')

    osc.bind(mainObj.grid16.editGrid, '/grid16/pattern_grid/edit')
    osc.bind(mainObj.grid16.editMidi, '/grid16/midi_params')
    osc.bind(mainObj.grid16.editPatternSeqLength, '/grid16/pattern_seq/length')
    osc.bind(mainObj.grid16.editPatternSeq, '/grid16/pattern_seq')

    osc.bind(mainObj.grid32.editGrid, '/grid32/pattern_grid/edit')
    osc.bind(mainObj.grid32.editMidi, '/grid32/midi_params')
    osc.bind(mainObj.grid32.editPatternSeqLength, '/grid32/pattern_seq/length')
    osc.bind(mainObj.grid32.editPatternSeq, '/grid32/pattern_seq')
   
    osc.bind(mainObj.menu.trackInfo, '/main/track_info')

    osc.bind(mainObj.menu.seqStepNumber, '/main/stepnumber')

    
    loop = True
    while loop:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                loop = False
            if event.type == pygame.MOUSEBUTTONUP :
                mousePosition = pygame.mouse.get_pos()
                mainObj.modeObject.mouseInput('up',mousePosition)
                
            if event.type == pygame.MOUSEBUTTONDOWN :
                mousePosition = pygame.mouse.get_pos()
                mainObj.modeObject.mouseInput('down',mousePosition)
                
            if event.type == pygame.MOUSEMOTION :
                mousePosition = pygame.mouse.get_pos()
                mainObj.modeObject.mouseInput('drag',mousePosition)
        
        mainObj.drawStuff()


    osc.dontListen()
    pygame.quit()



if __name__ == '__main__':
    main()
