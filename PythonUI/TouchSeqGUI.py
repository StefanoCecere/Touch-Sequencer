#!/usr/bin/env python

#Import Modules
import os, pygame, osc

from multigrid import *
from curve import *

from pygame.locals import *
from pygame.compat import geterror
    
class MainMenu():

    def __init__(self):
        self.mainBG, self.mainBGrect = load_image('mainMenu.png','backgrounds')
        self.gobutton, self.gobuttonrect = load_image('gobutton.png','buttons')
        self.stopbutton, self.stopbuttonrect = load_image('stopbutton.png','buttons')
        
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
        if track < 7:
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
        elif 6 < track < 10:
            sendOSCMessage('/curve/track_select', [track + 1])
            sendOSCMessage('/curve/track/get/curve', [1])
            sendOSCMessage('/curve/track/edit/curve_number', [1])
            mainObj.modeChange(3)


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

#    print address, value

#    osc.sendMsg(address, value, '192.168.2.3', 9002)
    osc.sendMsg(address, value, '127.0.0.1', 9004)


class Globject():

    def __init__(self):
        self.screen = pygame.display.set_mode((1024, 600))
        background = pygame.Surface(self.screen.get_size())
        self.background = background.convert()
        
        self.mode = 1
        
        self.curve       = CurveTrack()
        self.grid      = GridTrack()
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
            if mode == 1:
                self.modeObject = self.menu
            elif mode == 2:
                self.modeObject = self.grid
            elif mode == 3:
                self.modeObject = self.curve



def printStuff(*msg):
    '''deals with 'print' tagged OSC addresses '''

    print 'printing in the printStuff function ', msg
    print 'the oscaddress is ', msg[0][0]
    print 'the value is ', msg[0][2]




def main():


    global mainObj

    pygame.init()

    osc.init()
    osc.listen('127.0.0.1', 9001)

    mainObj = Globject()
    
    clock = pygame.time.Clock()

    osc.bind(mainObj.curve.editCurve, '/curve/gui_curve/edit') 
    osc.bind(mainObj.curve.editMidi, '/curve/midi_params')
    osc.bind(mainObj.curve.editLengths, '/curve/curve_lengths')
    osc.bind(mainObj.curve.editPlayStates, '/curve/play_states')

    osc.bind(mainObj.grid.editGrid, '/grid/pattern_grid/edit')
    osc.bind(mainObj.grid.editMidi, '/grid/midi_params')
    osc.bind(mainObj.grid.editPatternSeqLength, '/grid/pattern_seq/length')
    osc.bind(mainObj.grid.editPatternSeq, '/grid/pattern_seq')
    
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
