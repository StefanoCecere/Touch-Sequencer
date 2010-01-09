import os, pygame, __main__, bresenhams


class CurveTrack():

    def __init__(self):
        self.button1, self.button1rect               = __main__.load_image('button1.bmp','buttons')
        self.button2, self.button1rect               = __main__.load_image('button2.bmp','buttons')
        self.navButton1, self.navButton1rect         = __main__.load_image('navButton1.bmp','buttons')
        self.navButton2, self.navButton2rect         = __main__.load_image('navButton2.bmp','buttons')
        self.navButtonWide1, self.navButtonWide1rect = __main__.load_image('navButtonWide1.bmp','buttons')
        self.navButtonWide2, self.navButtonWide2rect = __main__.load_image('navButtonWide2.bmp','buttons')
        self.optionsbg, self.optionsbgrect           = __main__.load_image('curveOptsBG.bmp','backgrounds')
        self.gobutton, self.gobuttonrect             = __main__.load_image('gobutton.bmp','buttons')
        self.stopbutton, self.stopbuttonrect         = __main__.load_image('stopbutton.bmp','buttons')

        self.curveArray = [0 for curveVal in range(256)]
        self.ccNumbers   = [0 for numbers in range(8)]
        self.ccLengths   = [1 for numbers in range(8)]


        self.updateValue      = -1
        self.newValue         = 0
        self.oldValue         = 0
        
        self.playing          = 0
        self.midiChannel      = 1
        self.patternNumber    = 0
        
        self.mouseDown = 0
        
        self.trackMode = 'curve'
        
        self.black = 0, 0, 0
        self.prevPos = (0, 0)
        
        self.trackSurface = pygame.Surface((1024,600))
        self.trackSurface = self.trackSurface.convert()
        self.trackSurface.fill((250, 250, 250))

    
    # display functions
    
    def drawCurve(self):
        print 'curve array', self.curveArray
        pointList = []
        for data in range(256):
            dataVal = (512 - (self.curveArray[data] * 4))
            point = (data * 4), dataVal
            pointList.append(point)
            
        if len(pointList) > 1:
            pygame.draw.lines(self.curveSurface, self.black, False, pointList)

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
        for ccnumber in range(8):
            ccval = str(self.ccNumbers[ccnumber])
            font = pygame.font.Font(None, 62)
            displaytext = font.render(ccval, 1, (255, 255, 255))
            textpos = ((550 + 4),((ccnumber * 48) + 32 + 6))
            self.trackSurface.blit(displaytext, textpos)
        
        channel = str(self.midiChannel)
        font = pygame.font.Font(None, 96)
        displaytext = font.render(channel, 1, (255, 255, 255))
        textpos = (869,(354 + 2))
        self.trackSurface.blit(displaytext, textpos)
        
        ccval = str(self.newValue)
        font = pygame.font.Font(None, 96)
        ccvaltext = font.render(ccval, 1, (255, 255, 255))
        textpos = (709,(222 + 4))
        self.trackSurface.blit(ccvaltext, textpos)

    def drawCurveLengths(self):
        for row in range(8):
            for col in range(8):
                if (self.ccLengths[row]) < col:
                    self.trackSurface.blit(self.button2, ((col * 64),(row * 64)))
                else:
                    self.trackSurface.blit(self.button1, ((col * 64),(row * 64)))

    def drawPlayButton(self):
        buttonval = __main__.mainObj.menu.playingTracks[__main__.mainObj.menu.trackNo]
        if buttonval == 0:
            self.trackSurface.blit(self.stopbutton, (864,256))
        elif buttonval == 1:
            self.trackSurface.blit(self.gobutton, (864,256))

    def drawCurveScreen(self):
        self.trackSurface.fill((250, 250, 250))
        self.drawCurve()
        self.drawNavButtons()

    def drawOptionsScreen(self):
        self.trackSurface.fill((250, 250, 250))
        self.drawCurveLengths()
        self.drawMidiOptions()
        self.drawNavButtons()
        self.drawPlayButton()


    # functions that will be called from OSC messages


    def updateCurveLength(self, col, row):
        self.cclengths[row] = col
        data = [row, col]
        __main__.sendOSCMessage('/curve/track/edit/pattern_seq', data)

    def mouseInput(self, type, pos):
        if self.trackMode == 'curve':
            self.inputCurveScreen(type, pos)
        elif self.trackMode == 'options' && type == 'down':
            self.inputOptionsScreen(pos)

    def inputCurveScreen(self, type, pos):
        xval = pos[0]
        yval = pos[1]
        if yval < 512:
            if type == 'down':
                self.mouseDown = 1
                xval = pos[0]
                yval = (512 - pos[1])
                xval = int(round(xval / 4))
                yval = int(round(yval / 4))
                self.prevPos = (xval, yval)
            elif type == 'drag' and self.mouseDown == 1:            
                xval = pos[0]
                yval = (512 - pos[1])
                xval = int(round(xval / 4))
                yval = int(round(yval / 4))
                
                currentPos = (xval,yval)
                
                smoothPoints = bresenhams.smoothLine(currentPos, self.prevPos)
                
                for points in smoothPoints:
                    xval = points[0]
                    yval = points[1]
                    self.curveArray[xval] = yval
                
                self.prevPos = currentPos
                
                self.curveSurface.blit(self.mainBG, (0,0))
                self.drawLines()
            elif type == 'up':
                self.mouseDown = 0
        else:
            self.mouseDown = 0
            self.navButtonInterface(int(round(xval / 64)))

    def editCurve(self, *msg):
        if msg[0][2] == 'clear':
            self.clearCurve()
        else:
            xval = (msg[0][2])
            yval = (msg[0][3])
            self.curveArray[xval] = yval

    def clearCurve(self):
        for curveVal in range(256):
            self.curveArray[curveVal] = 0

    def editMidi(self, *msg):
        param = msg[0][2]
        if param == 'ccnumber':
            ccnumber = (msg[0][3] - 1)
            self.ccNumbers[ccnumber] = msg[0][4]
        elif param == 'velocity':
            self.midiVelocity = msg[0][3]
        elif param == 'channel':
            self.midiChannel = msg[0][3]
        elif param == 'length':
            self.midiLength = msg[0][3]


    # mouse input functions

    
    def navButtonInterface(self, col):
        if col < 8:
            __main__.sendOSCMessage('/curve/track/get/curve', [col])
            __main__.sendOSCMessage('/curve/track/edit/curvenumber', [col])
            self.curvepattern = col
            self.patternNumber = col
            self.trackMode = 'curve'
        elif col == 8 or col == 9:
            self.patternNumber = 8
            self.trackMode = 'options'
            __main__.sendOSCMessage('/curve/track/get/pattern_seq',['bang'])
            __main__.sendOSCMessage('/curve/track/get/pattern_seq_length',['bang'])
            __main__.sendOSCMessage('/curve/track/get/all_midi_params',['bang'])
        elif col == 10 or col == 11:
            blah = 1
        elif col == 12 or col == 13:
            blah = 1
        elif col == 14 or col == 15:
            self.patternNumber = 0
            self.trackMode = 'curve'
            __main__.mainObj.modeChange(1)

    def inputMidiOptions(self, pos):
        xval = pos[0]
        yval = pos[1]
        col = int(round(xval / 32))
        row = int(round(yval / 32))
        if 16 < col < 21 and 0 < row < 13:
            ccnumber = ((yval - 32) / 48)
            self.updateValue = ccnumber
            self.oldValue = self.ccNumbers[ccnumber]
            print 'cc number', ccnumber
        elif 21 < col < 31 and 0 < row < 7:
            self.keypadPress(col, row)
        elif 21 < col < 26 and 10 < row < 13:
            print 'velocity'
            self.oldValue = self.midiVelocity
            self.updateValue = 8
        elif 26 < col < 31 and 10 < row < 13:
            print 'Length'
            self.oldValue = self.midiLength
            self.updateValue = 9
        elif 26 < col < 31 and 7 < row < 10:
            self.updateValue = -1
            playval = __main__.mainObj.menu.playingTracks[__main__.mainObj.menu.trackNo]
            if playval == 0:
                __main__.mainObj.menu.playingTracks[__main__.mainObj.menu.trackNo] = 1
                __main__.sendOSCMessage('/curve/track/control/play', [1])
            if playval == 1:
                __main__.mainObj.menu.playingTracks[__main__.mainObj.menu.trackNo] = 0
                __main__.sendOSCMessage('/curve/track/control/play', [0])
        else:
            self.updateValue = -1

    def keypadPress(self, col, row):
        if self.updateValue != -1:
            if 0 < row < 3:
                if 21 < col < 24:
                    print '1'
                    self.newValue *= 10
                    self.newValue += 1
                if 23 < col < 26:
                    print '2'
                    self.newValue *= 10
                    self.newValue += 2
                if 25 < col < 28:
                    print '3'
                    self.newValue *= 10
                    self.newValue += 3
                if 27 < col < 31:
                    print 'enter'
                    if self.updateValue < 8:
                        if self.newValue > 127:
                            self.updateValue = -1
                            self.newValue = 0
                        else:
                            self.ccNumbers[self.updateValue] = self.newValue
                            data = [self.updateValue + 1, self.newValue]
                            __main__.sendOSCMessage('/curve/track/edit/ccnumber', data)
                    elif self.updateValue == 8:
                        if self.newValue > 127:
                            self.updateValue = -1
                            self.newValue = 0
                        else:
                            self.midiVelocity = self.newValue
                            data = [self.newValue]
                            __main__.sendOSCMessage('/curve/track/edit/midi_params/velocity', data)
                    elif self.updateValue == 9:
                        if self.newValue > 999:
                            self.updateValue = -1
                            self.newValue = 0
                        else:
                            self.midiLength = self.newValue
                            data = [self.newValue]
                            __main__.sendOSCMessage('/curve/track/edit/midi_params/length', data)
                    self.updateValue = -1
                    self.newValue = 0
            if 2 < row < 5:
                if 21 < col < 24:
                    print '4'
                    self.newValue *= 10
                    self.newValue += 4
                if 23 < col < 26:
                    print '5'
                    self.newValue *= 10
                    self.newValue += 5
                if 25 < col < 28:
                    print '6'
                    self.newValue *= 10
                    self.newValue += 6
                if 27 < col < 31:
                    print 'cancel'
                    self.updateValue = -1
                    self.newValue = 0
            if 4 < row < 7:
                if 21 < col < 24:
                    print '7'
                    self.newValue *= 10
                    self.newValue += 7
                if 23 < col < 26:
                    print '8'
                    self.newValue *= 10
                    self.newValue += 8
                if 25 < col < 28:
                    print '9'
                    self.newValue *= 10
                    self.newValue += 9
                if 27 < col < 30:
                    print '0'
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
        elif self.trackMode == 'curve':
            self.drawGridScreen()
        return self.trackSurface


