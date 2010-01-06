import os, pygame, __main__


class GridTrack():

    def __init__(self):
        self.button1, self.button1rect               = __main__.load_image('button1.bmp','buttons')
        self.button2, self.button1rect               = __main__.load_image('button2.bmp','buttons')
        self.navButton1, self.navButton1rect         = __main__.load_image('navButton1.bmp','buttons')
        self.navButton2, self.navButton2rect         = __main__.load_image('navButton2.bmp','buttons')
        self.navButtonWide1, self.navButtonWide1rect = __main__.load_image('navButtonWide1.bmp','buttons')
        self.navButtonWide2, self.navButtonWide2rect = __main__.load_image('navButtonWide2.bmp','buttons')
        self.optionsbg, self.optionsbgrect           = __main__.load_image('optionsBG.bmp','backgrounds')
        self.gobutton, self.gobuttonrect             = __main__.load_image('gobutton.bmp','buttons')
        self.stopbutton, self.stopbuttonrect         = __main__.load_image('stopbutton.bmp','buttons')
        
        self.trackgrid   = [[0 for row in range(8)] for col in range(16)]
        self.patterngrid = [0 for col in range(8)]
        self.midinotes   = [0 for notes in range(8)]
        
        self.updateValue      = -1
        self.newValue         = 0
        self.oldValue         = 0
        
        self.gridpattern      = 0

        self.playing          = 0
        self.midiLength       = 1
        self.midiVelocity     = 1
        self.midiChannel      = 1
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
            font = pygame.font.Font(None, 62)
            notetext = font.render(noteval, 1, (255, 255, 255))
            textpos = ((550 + 4),((note * 48) + 32 + 6))
            self.trackSurface.blit(notetext, textpos)
        
        noteval = str(self.midiLength)
        font = pygame.font.Font(None, 96)
        notetext = font.render(noteval, 1, (255, 255, 255))
        textpos = (709,(354 + 2))
        self.trackSurface.blit(notetext, textpos)
        
        noteval = str(self.midiVelocity)
        font = pygame.font.Font(None, 96)
        notetext = font.render(noteval, 1, (255, 255, 255))
        textpos = (869,(354 + 2))
        self.trackSurface.blit(notetext, textpos)
        
        noteval = str(self.newValue)
        font = pygame.font.Font(None, 96)
        notetext = font.render(noteval, 1, (255, 255, 255))
        textpos = (709,(222 + 4))
        self.trackSurface.blit(notetext, textpos)

    def drawPatternSeq(self):
        for col in range(8):
            for row in range(8):
                if (self.patterngrid[col]) == row:
                    self.trackSurface.blit(self.button1, ((col * 64),(row * 64)))
                else:
                    self.trackSurface.blit(self.button2, ((col * 64),(row * 64)))

    def drawPlayButton(self):
        buttonval = __main__.mainObj.menu.playingTracks[__main__.mainObj.menu.trackNo]
        if buttonval == 0:
            self.trackSurface.blit(self.stopbutton, (864,256))
        elif buttonval == 1:
            self.trackSurface.blit(self.gobutton, (864,256))

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
        __main__.sendOSCMessage('/grid/track/edit/pattern_grid', data)

    def updatePatternSeq(self, col, row):
        self.patterngrid[col] = row
        data = [col, (7 - row)]
        __main__.sendOSCMessage('/grid/track/edit/pattern_seq', data)

    def updatePatternSeqLength(self, col):
        self.patternSeqLength = (col - 7)
        __main__.sendOSCMessage('/grid/track/edit/pattern_seq_length', [self.patternSeqLength])

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

    def editMidi(self, *msg):
        param = msg[0][2]
        if param == "notes":
            notenum = (msg[0][3] - 1)
            self.midinotes[notenum] = msg[0][4]
        elif param == "velocity":
            self.midiVelocity = msg[0][3]
        elif param == "channel":
            self.midiChannel = msg[0][3]
        elif param == "length":
            self.midiLength = msg[0][3]


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
            __main__.sendOSCMessage('/grid/track/get/pattern_grid', [col])
            __main__.sendOSCMessage('/grid/track/edit/pattern_number', [col])
            self.gridpattern = col
            self.patternNumber = col
            self.trackMode = 'grid'
        elif col == 8 or col == 9:
            self.patternNumber = 8
            self.trackMode = 'options'
            __main__.sendOSCMessage('/grid/track/get/pattern_seq',["bang"])
            __main__.sendOSCMessage('/grid/track/get/pattern_seq_length',["bang"])
            __main__.sendOSCMessage('/grid/track/get/all_midi_params',["bang"])
        elif col == 10 or col == 11:
            blah = 1
        elif col == 12 or col == 13:
            blah = 1
        elif col == 14 or col == 15:
            self.patternNumber = 0
            self.trackMode = 'grid'
            __main__.mainObj.modeChange(1)

    def inputMidiOptions(self, pos):
        xval = pos[0]
        yval = pos[1]
        col = int(round(xval / 32))
        row = int(round(yval / 32))
        if 16 < col < 21 and 0 < row < 13:
            note = ((yval - 32) / 48)
            self.updateValue = note
            self.oldValue = self.midinotes[note]
            print "midi note", note
        elif 21 < col < 31 and 0 < row < 7:
            self.keypadPress(col, row)
        elif 21 < col < 26 and 10 < row < 13:
            print "velocity"
            self.oldValue = self.midiVelocity
            self.updateValue = 8
        elif 26 < col < 31 and 10 < row < 13:
            print "Length"
            self.oldValue = self.midiLength
            self.updateValue = 9
        elif 26 < col < 31 and 7 < row < 10:
            self.updateValue = -1
            playval = __main__.mainObj.menu.playingTracks[__main__.mainObj.menu.trackNo]
            if playval == 0:
                __main__.mainObj.menu.playingTracks[__main__.mainObj.menu.trackNo] = 1
                __main__.sendOSCMessage('/grid/track/control/play', [1])
            if playval == 1:
                __main__.mainObj.menu.playingTracks[__main__.mainObj.menu.trackNo] = 0
                __main__.sendOSCMessage('/grid/track/control/play', [0])
        else:
            self.updateValue = -1

    def keypadPress(self, col, row):
        if self.updateValue != -1:
            if 0 < row < 3:
                if 21 < col < 24:
                    print "1"
                    self.newValue *= 10
                    self.newValue += 1
                if 23 < col < 26:
                    print "2"
                    self.newValue *= 10
                    self.newValue += 2
                if 25 < col < 28:
                    print "3"
                    self.newValue *= 10
                    self.newValue += 3
                if 27 < col < 31:
                    print "enter"
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
                        if self.newValue > 999:
                            self.updateValue = -1
                            self.newValue = 0
                        else:
                            self.midiLength = self.newValue
                            data = [self.newValue]
                            __main__.sendOSCMessage('/grid/track/edit/midi_params/length', data)
                    self.updateValue = -1
                    self.newValue = 0
            if 2 < row < 5:
                if 21 < col < 24:
                    print "4"
                    self.newValue *= 10
                    self.newValue += 4
                if 23 < col < 26:
                    print "5"
                    self.newValue *= 10
                    self.newValue += 5
                if 25 < col < 28:
                    print "6"
                    self.newValue *= 10
                    self.newValue += 6
                if 27 < col < 31:
                    print "cancel"
                    self.updateValue = -1
                    self.newValue = 0
            if 4 < row < 7:
                if 21 < col < 24:
                    print "7"
                    self.newValue *= 10
                    self.newValue += 7
                if 23 < col < 26:
                    print "8"
                    self.newValue *= 10
                    self.newValue += 8
                if 25 < col < 28:
                    print "9"
                    self.newValue *= 10
                    self.newValue += 9
                if 27 < col < 30:
                    print "0"
                    self.newValue *= 10


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

    def drawScreen(self):
        if self.trackMode == 'options':
            self.drawOptionsScreen()
        elif self.trackMode == 'grid':
            self.drawGridScreen()
        return self.trackSurface


