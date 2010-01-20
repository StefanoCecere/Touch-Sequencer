import os, pygame, __main__

class GridTrack():

    def __init__(self):
        self.button1, self.button1rect               = __main__.load_image('button1.png','buttons')
        self.button2, self.button1rect               = __main__.load_image('button2.png','buttons')
        self.button3, self.button1rect               = __main__.load_image('button3.png','buttons')
        self.button4, self.button1rect               = __main__.load_image('button4.png','buttons')
        self.button5, self.button1rect               = __main__.load_image('button5.png','buttons')
        
        self.navButton1, self.navButton1rect         = __main__.load_image('navButton1.png','buttons')
        self.navButton2, self.navButton2rect         = __main__.load_image('navButton2.png','buttons')
        self.navButtonWide1, self.navButtonWide1rect = __main__.load_image('navButtonWide1.png','buttons')
        self.navButtonWide2, self.navButtonWide2rect = __main__.load_image('navButtonWide2.png','buttons')
        self.optionsbg, self.optionsbgrect           = __main__.load_image('optionsBG.png','backgrounds')
        self.gobutton, self.gobuttonrect             = __main__.load_image('optsButtonGreen.png','buttons')
        self.stopbutton, self.stopbuttonrect         = __main__.load_image('optsButtonRed.png','buttons')
        
        self.trackgrid   = [[0 for row in range(8)] for col in range(16)]
        self.patterngrid = [0 for col in range(8)]
        self.midinotes   = [0 for notes in range(8)]
        
        self.updateValue      = -1
        self.newValue         = 0
        
        self.gridpattern      = 0

        self.playing          = 0
        self.midiLength       = 1
        self.midiVelocity     = 1
        self.midiChannel      = 1
        
        self.swingType        = '8'
        self.swingAmount      = 100
        
        self.patternSeqLength = 1
        self.patternNumber    = 0
        
        self.fontName         = pygame.font.match_font('arial')
        
        self.mode             = 'grid'
        
        self.followMode       = 0
        
        self.trackSurface = pygame.Surface((1024,600))
        self.trackSurface = self.trackSurface.convert()
        self.trackSurface.fill((250, 250, 250))

    # functions callable from outside the object

    def mouseInput(self, type, pos):
        if type == 'down':
            if self.mode == 'grid':
                self.inputGridScreen(pos)
            elif self.mode == 'options':
                self.inputOptionsScreen(pos)

    def drawScreen(self):
        if self.mode == 'options':
            self.drawOptionsScreen()
        elif self.mode == 'grid':
            self.drawGridScreen()
        return self.trackSurface

    def trackSetup(self):
        __main__.sendOSCMessage('/grid/track/get/pattern_grid', [0])
  
    # display functions
    
    def drawGrid(self):
        for col in range(16):
            for row in range(8):
                buttonval = self.trackgrid[col][row]
                if self.followMode == 1:
                    if col == __main__.mainObj.menu.stepNumber:
                        buttonval += 3
                        
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
            font = pygame.font.Font(self.fontName, 50)
            notetext = font.render(noteval, 1, (255, 255, 255))
            textpos = ((512 + 32 + 4),((note * 48) + 32 - 4))
            self.trackSurface.blit(notetext, textpos)
        
        noteval = str(self.midiVelocity)
        font = pygame.font.Font(self.fontName, 70)
        notetext = font.render(noteval, 1, (255, 255, 255))
        textpos = (710,(64 - 7))
        self.trackSurface.blit(notetext, textpos)
        
        noteval = str(self.midiChannel)
        font = pygame.font.Font(self.fontName, 70)
        notetext = font.render(noteval, 1, (255, 255, 255))
        textpos = (710,(160 - 7))
        self.trackSurface.blit(notetext, textpos)
        
        noteval = str(self.midiLength)
        font = pygame.font.Font(self.fontName, 70)
        notetext = font.render(noteval, 1, (255, 255, 255))
        textpos = (710,(256 - 7))
        self.trackSurface.blit(notetext, textpos)
        
        noteval = str(self.newValue)
        font = pygame.font.Font(self.fontName, 34)
        notetext = font.render(noteval, 1, (255, 255, 255))
        textpos = (866,(130 - 6))
        self.trackSurface.blit(notetext, textpos)
        
        noteval = str(self.swingAmount)
        font = pygame.font.Font(self.fontName, 70)
        notetext = font.render(noteval, 1, (255, 255, 255))
        textpos = (870,(352 - 7))
        self.trackSurface.blit(notetext, textpos)
        
        noteval = str(self.swingType)
        font = pygame.font.Font(self.fontName, 70)
        notetext = font.render(noteval, 1, (255, 255, 255))
        textpos = (870,(256 - 7))
        self.trackSurface.blit(notetext, textpos)

    def drawPatternSeq(self):
        for col in range(8):
            for row in range(8):
                if (self.patterngrid[col]) == 7 - row:
                    self.trackSurface.blit(self.button2, ((col * 64),(row * 64)))
                else:
                    self.trackSurface.blit(self.button1, ((col * 64),(row * 64)))

    def drawPlayButton(self):
        buttonval = __main__.mainObj.menu.playingTracks[__main__.mainObj.menu.trackNo]
        if buttonval == 0:
            self.trackSurface.blit(self.stopbutton, (704,352))
        elif buttonval == 1:
            self.trackSurface.blit(self.gobutton, (704,352))

    def drawPatternSeqLength(self):
        for seqlength in range(8):
            if seqlength < self.patternSeqLength:
                xval = ((seqlength * 64) + (8 * 64))
                yval = (7 * 64)
                self.trackSurface.blit(self.button2, (xval,yval))
            else:
                xval = ((seqlength * 64) + (8 * 64))
                yval = (7 * 64)
                self.trackSurface.blit(self.button1, (xval,yval))


    def drawGridScreen(self):
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
    
    def updateGridButton(self, col, row):
        data = [row + 1, col + 1, self.trackgrid[col][row]]
        __main__.sendOSCMessage('/grid/track/edit/pattern_grid', data)

    def updatePatternSeq(self, col, row):
        self.patterngrid[col] = (7 - row)
        data = [col, (7 - row)]
        __main__.sendOSCMessage('/grid/track/edit/pattern_seq', data)

    def updatePatternSeqLength(self, col):
        self.patternSeqLength = (col - 7)
        __main__.sendOSCMessage('/grid/track/edit/pattern_seq_length', [self.patternSeqLength])

    def editPatternSeq(self, *msg):
        xval = msg[0][2]
        yval = msg[0][3]
        self.patterngrid[xval] = yval

    def editPatternSeqLength(self, *msg):
        length = msg[0][2]
        self.patternSeqLength = length

    def editGrid(self, *msg):
        if msg[0][2] == 'clear':
            self.clearGrid()
        else:
            yval = (msg[0][2] - 1)
            xval = (msg[0][3] - 1)
            if yval >= 0 and xval >= 0:
                dval = msg[0][4]
                self.trackgrid[xval][yval] = dval

    def clearGrid(self):
        for col in range(16):
            for row in range(8):
                self.trackgrid[col][row] = 0

    def editMidi(self, *msg):
        param = msg[0][2]
        if param == 'notes':
            notenum = (msg[0][3] - 1)
            self.midinotes[notenum] = msg[0][4]
        elif param == 'velocity':
            self.midiVelocity = msg[0][3]
        elif param == 'channel':
            self.midiChannel = msg[0][3]
        elif param == 'length':
            self.midiLength = msg[0][3]


    # mouse input functions

    def inputGridScreen(self, pos):
        col = int(round(pos[0] / 64))
        row = int(round(pos[1] / 64))
        
        if row < 8:
            self.updateGridButton(col, row)
        else:
            self.navButtonInterface(col)

    
    def navButtonInterface(self, col):
        if col < 8:
            if self.followMode == 1:
                self.followMode = 0
                __main__.sendOSCMessage('/grid/track/edit/follow_mode',[0])
            
            __main__.sendOSCMessage('/grid/track/get/pattern_grid', [col])
            self.gridpattern = col
            self.patternNumber = col
            self.mode = 'grid'
        elif col == 8 or col == 9:
            if self.followMode == 1:
                self.followMode = 0
                __main__.sendOSCMessage('/grid/track/edit/follow_mode',[0])
                
            self.patternNumber = 8
            self.mode = 'options'
            __main__.sendOSCMessage('/grid/track/get/pattern_seq',['bang'])
            __main__.sendOSCMessage('/grid/track/get/pattern_seq_length',['bang'])
            __main__.sendOSCMessage('/grid/track/get/all_midi_params',['bang'])
        #    __main__.sendOSCMessage('/grid/track/get/swing_amount', ['bang'])
        #    __main__.sendOSCMessage('/grid/track/get/swing_amount', ['bang'])
        elif col == 10 or col == 11:
            if self.followMode == 0:
                self.followMode = 1
                __main__.sendOSCMessage('/grid/track/edit/follow_mode',[1])
            self.patternNumber = 8
            self.mode = 'grid'
        elif col == 12 or col == 13:
            pass
        elif col == 14 or col == 15:
            if self.followMode == 1:
                self.followMode = 0
                __main__.sendOSCMessage('/grid/track/edit/follow_mode',[0])
                
            self.patternNumber = 0
            self.mode = 'grid'
            __main__.mainObj.modeChange('main')

    def inputMidiOptions(self, pos):
        xval = pos[0]
        yval = pos[1]
        col = int(round(pos[0] / 32))
        row = int(round(pos[1] / 32))
        if 16 < col < 21 and 0 < row < 13:
            note = ((yval - 32) / 48)
            self.updateValue = note
        elif 26 < col < 31 and 0 < row < 5:
            self.keypadPress(xval - 864, yval - 32)
            
        elif 21 < col < 26 and 1 < row < 4:
            self.updateValue = 8
        elif 21 < col < 26 and 4 < row < 7:
            self.updateValue = 9
        elif 21 < col < 26 and 7 < row < 10:
            self.updateValue = 10
        elif 21 < col < 26 and 10 < row < 13:
            self.updateValue = -1
            playval = __main__.mainObj.menu.playingTracks[__main__.mainObj.menu.trackNo]
            if playval == 0:
                __main__.mainObj.menu.playingTracks[__main__.mainObj.menu.trackNo] = 1
                __main__.sendOSCMessage('/grid/track/control/play', [1])
            if playval == 1:
                __main__.mainObj.menu.playingTracks[__main__.mainObj.menu.trackNo] = 0
                __main__.sendOSCMessage('/grid/track/control/play', [0])
                
        elif 26 < col < 31 and 7 < row < 10:
            if self.swingType == '8':
                self.swingType = '16'
            #     __main__.sendOSCMessage('/grid/track/edit/swing_type', [0])
            else:
                self.swingType = '8'
            #     __main__.sendOSCMessage('/grid/track/edit/swing_type', [1])
        elif 26 < col < 31 and 10 < row < 13:
            self.updateValue = 11
        
        else:
            self.updateValue = -1

    def keypadPress(self, xval, yval):
        if self.updateValue != -1:
            col = int(round(xval / 32))
            row = int(round(yval / 32))
            if row == 0:
                if col == 0:
                    self.newValue *= 10
                    self.newValue += 1
                    if self.newValue > 999:
                        self.updateValue = -1
                        self.newValue = 0
                if col == 1:
                    self.newValue *= 10
                    self.newValue += 2
                    if self.newValue > 999:
                        self.updateValue = -1
                        self.newValue = 0
                if col == 2:
                    self.newValue *= 10
                    self.newValue += 3
                    if self.newValue > 999:
                        self.updateValue = -1
                        self.newValue = 0
                if col == 3:
                    if self.updateValue < 8:
                        if self.newValue > 127:
                            self.updateValue = -1
                            self.newValue = 0
                        else:
                            self.midinotes[self.updateValue] = self.newValue
                            data = [self.updateValue + 1, self.newValue]
                            __main__.sendOSCMessage('/grid/track/edit/notes', data)
                    elif self.updateValue == 8:
                        if self.newValue > 127:
                            self.updateValue = -1
                            self.newValue = 0
                        else:
                            self.midiVelocity = self.newValue
                            data = [self.newValue]
                            __main__.sendOSCMessage('/grid/track/edit/midi_params/velocity', data)
                    elif self.updateValue == 9:
                        if self.newValue > 16 or self.newValue < 1:
                            self.updateValue = -1
                            self.newValue = 0
                        else:
                            self.midiChannel = self.newValue
                            data = [self.newValue]
                            __main__.sendOSCMessage('/grid/track/edit/midi_params/channel', data)
                    elif self.updateValue == 10:
                        if self.newValue > 32 or self.newValue < 1:
                            self.updateValue = -1
                            self.newValue = 0
                        else:
                            self.midiLength = self.newValue
                            data = [self.newValue]
                            __main__.sendOSCMessage('/grid/track/edit/midi_params/length', data)
                    elif self.updateValue == 11:
                        if self.newValue > 100:
                            self.updateValue = -1
                            self.newValue = 0
                        else:
                            self.swingAmount = self.newValue
                            data = [self.newValue]
                        #    __main__.sendOSCMessage('/grid/track/edit/swing_amount', data)
                    self.updateValue = -1
                    self.newValue = 0
            if row == 1:
                if col == 0:
                    self.newValue *= 10
                    self.newValue += 4
                    if self.newValue > 999:
                        self.updateValue = -1
                        self.newValue = 0
                if col == 1:
                    self.newValue *= 10
                    self.newValue += 5
                    if self.newValue > 999:
                        self.updateValue = -1
                        self.newValue = 0
                if col == 2:
                    self.newValue *= 10
                    self.newValue += 6
                    if self.newValue > 999:
                        self.updateValue = -1
                        self.newValue = 0
                if col == 3:
                    self.updateValue = -1
                    self.newValue = 0
            if row == 2:
                if col == 0:
                    self.newValue *= 10
                    self.newValue += 7
                    if self.newValue > 999:
                        self.updateValue = -1
                        self.newValue = 0
                if col == 1:
                    self.newValue *= 10
                    self.newValue += 8
                    if self.newValue > 999:
                        self.updateValue = -1
                        self.newValue = 0
                if col == 2:
                    self.newValue *= 10
                    self.newValue += 9
                    if self.newValue > 999:
                        self.updateValue = -1
                        self.newValue = 0
                if col == 3:
                    self.newValue *= 10
                    if self.newValue > 999:
                        self.updateValue = -1
                        self.newValue = 0


    def inputOptionsScreen(self, pos):
        col = pos[0]
        row = pos[1]
        col = int(round(col / 64))
        row = int(round(row / 64))
        if row > 7:
            self.navButtonInterface(col)
            self.updateValue = -1
        elif col < 8:
            self.updatePatternSeq(col,row)
            self.updateValue = -1
        elif row == 7:
            self.updatePatternSeqLength(col)
            self.updateValue = -1
        else:
            self.inputMidiOptions(pos)




