import os, pygame, __main__, bresenhams


class CurveTrack():

    def __init__(self):
        self.curvebg, self.curvebgrect               = __main__.load_image('curvebg.png','backgrounds')
        self.button1, self.button1rect               = __main__.load_image('button1.png','buttons')
        self.button2, self.button1rect               = __main__.load_image('button2.png','buttons')
        self.navButton1, self.navButton1rect         = __main__.load_image('navButton1.png','buttons')
        self.navButton2, self.navButton2rect         = __main__.load_image('navButton2.png','buttons')
        self.navButtonWide1, self.navButtonWide1rect = __main__.load_image('navButtonWide1.png','buttons')
        self.navButtonWide2, self.navButtonWide2rect = __main__.load_image('navButtonWide2.png','buttons')
        self.optionsbg, self.optionsbgrect           = __main__.load_image('curveOptsBG.png','backgrounds')
        self.gobutton, self.gobuttonrect             = __main__.load_image('gobutton.png','buttons')
        self.stopbutton, self.stopbuttonrect         = __main__.load_image('stopbutton.png','buttons')

        self.curveArray  = [0 for curveVal in range(256)]
        
        self.ccNumbers   = [0 for numbers in range(8)]
        self.ccChannel   = [0 for numbers in range(8)]
        self.ccPlaying   = [0 for numbers in range(8)]
        self.ccLengths   = [1 for numbers in range(8)]


        self.updateValue      = 'none'
        self.updatecc         = -1
        self.newValue         = 0
        self.oldValue         = 0
        
        self.patternNumber    = 0
        
        self.mouseDown = 0
        
        self.trackMode = 'curve'
        
        self.black = 0, 0, 0
        self.prevPos = (0, 0)
        
        self.trackSurface = pygame.Surface((1024,600))
        self.trackSurface = self.trackSurface.convert()
        self.trackSurface.fill((250, 250, 250))

    
    # display functions
    
    def drawScreen(self):
        if self.trackMode == 'options':
            self.drawOptionsScreen()
        elif self.trackMode == 'curve':
            self.drawCurveScreen()
        return self.trackSurface
    
    def drawCurve(self):
        pointList = []
        for data in range(256):
            dataVal = (512 - (self.curveArray[data] * 4))
            point = (data * 4), dataVal
            pointList.append(point)
            
        if len(pointList) > 1:
            pygame.draw.lines(self.trackSurface, self.black, False, pointList)

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
        self.trackSurface.blit(self.optionsbg, (0,0))
        for ccnumber in range(8):
        
            ccval = str(self.ccNumbers[ccnumber])
            font = pygame.font.Font(None, 62)
            displaytext = font.render(ccval, 1, (255, 255, 255))
            textpos = ((64 + 4),((ccnumber * 48) + 64 + 6))
            self.trackSurface.blit(displaytext, textpos)
        
            channel = str(self.ccChannel[ccnumber])
            font = pygame.font.Font(None, 62)
            displaytext = font.render(channel, 1, (255, 255, 255))
            textpos = ((192 + 4),((ccnumber * 48) + 64 + 6))
            self.trackSurface.blit(displaytext, textpos)
        
            length = str(self.ccLengths[ccnumber])
            font = pygame.font.Font(None, 62)
            displaytext = font.render(length, 1, (255, 255, 255))
            textpos = ((320 + 4),((ccnumber * 48) + 64 + 6))
            self.trackSurface.blit(displaytext, textpos)
        
            buttonval = self.ccPlaying[ccnumber]
            if buttonval == 0:
                self.trackSurface.blit(self.stopbutton, ((448 + 4),((ccnumber * 48) + 64)))
            elif buttonval == 1:
                self.trackSurface.blit(self.gobutton, ((448 + 4),((ccnumber * 48) + 64)))

        ccval = str(self.newValue)
        font = pygame.font.Font(None, 96)
        ccvaltext = font.render(ccval, 1, (255, 255, 255))
        textpos = (709,(222 + 4))
        self.trackSurface.blit(ccvaltext, textpos)

    def drawCurveScreen(self):
        self.trackSurface.blit(self.curvebg, (0,0))
        self.drawCurve()
        self.drawNavButtons()

    def drawOptionsScreen(self):
        self.trackSurface.fill((250, 250, 250))
        self.drawMidiOptions()
        self.drawNavButtons()

    #functions for OSC communication

    def sendCurveData(self):
        temparray = [0 for curveVal in range(259)]
        temparray[0] = self.curveArray[0]
        for curveVal in range(256):
            temparray[curveVal + 1] = self.curveArray[curveVal]
        temparray[257] = self.curveArray[255]
        temparray[258] = self.curveArray[255]
        datastring = map(str, temparray)
        data = [' '.join(datastring)]
        print data
        __main__.sendOSCMessage('/curve/track/edit/curve', data)

    def editCurve(self, *msg):
        info = msg[0][2].split()
        temparray = map(int, info)
        del temparray [0]
        del temparray[-1]
        del temparray[-1]
        self.curveArray = temparray


    def clearCurve(self):
        for curveVal in range(256):
            self.curveArray[curveVal] = 0

    def editMidi(self, *msg):
        val    = msg[0][4]
        numb   = msg[0][3]
        param  = msg[0][2]
        if param == 'ccnumber':
            self.ccNumbers[numb - 1] = val
        elif param == 'channel':
            self.midiChannel[numb - 1] = val

    def editLengths(self, *msg):
        val    = msg[0][3]
        numb   = msg[0][2]
        self.ccLengths[numb - 1] = val



    # mouse input functions

    def mouseInput(self, type, pos):
        if self.trackMode == 'curve':
            self.inputCurveScreen(type, pos)
        elif self.trackMode == 'options' and type == 'down':
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
                
                self.drawLines()
            elif type == 'up':
                if self.mouseDown == 1:
                    self.mouseDown = 0
                    self.sendCurveData()
        else:
            if self.mouseDown == 1:
                self.mouseDown = 0
                self.sendCurveData()
            if type == 'down':
                self.navButtonInterface(int(round(xval / 64)))

    def drawLines(self):
        print 'curve array', self.curveArray
        pointList = []
        for data in range(256):
            dataVal = (512 - (self.curveArray[data] * 4))
            point = (data * 4), dataVal
            pointList.append(point)
            
        if len(pointList) > 1:
            pygame.draw.lines(self.trackSurface, self.black, False, pointList)

    def navButtonInterface(self, col):
        if col < 8:
            __main__.sendOSCMessage('/curve/track/get/curve', [col + 1])
            __main__.sendOSCMessage('/curve/track/edit/curve_number', [col + 1])
            self.curvepattern = col
            self.patternNumber = col
            self.trackMode = 'curve'
        elif col == 8 or col == 9:
            self.patternNumber = 8
            self.trackMode = 'options'
            __main__.sendOSCMessage('/curve/track/get/curve_length',['bang'])
            __main__.sendOSCMessage('/curve/track/get/midi_params/cc_number',['bang'])
            __main__.sendOSCMessage('/curve/track/get/midi_params/midi_channel',['bang'])
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
        col = int(round(xval / 64))
        row = int(round(yval / 64))
        if 0 < col < 7:
            ccnumber = ((yval - 64) / 48)
            
            if 0 < row < 3:
                self.updatecc = ccnumber
                self.updateValue = 'number'
                self.oldValue = self.ccNumbers[ccnumber]
                print 'cc number', ccnumber
            
            elif 2 < row < 5:
                self.updatecc = ccnumber
                self.updateValue = 'length'
                self.oldValue = self.ccNumbers[ccnumber]
                print 'cc length', ccnumber
            
            elif 4 < row < 7:
                self.updatecc = ccnumber
                self.updateValue = 'channel'
                self.oldValue = self.ccNumbers[ccnumber]
                print 'cc channel', ccnumber
            
            elif 6 < row < 9:
                if self.ccPlaying[ccnumber] == 1:
                    self.ccPlaying[ccnumber] = 0
                    data = [ccnumber + 1, 0]
                    __main__.sendOSCMessage('/curve/track/control/curve_play', data)
                elif self.ccPlaying[ccnumber] == 0:
                    self.ccPlaying[ccnumber] = 1
                    data = [ccnumber + 1, 1]
                    __main__.sendOSCMessage('/curve/track/control/curve_play', data)
            print 'cc play', ccnumber
            
        elif 9 < col < 15 and 1 < row < 6:
            self.keypadPress(xval - 640, yval - 128)
        else:
            self.updateValue = 'none'

    def keypadPress(self, xval, yval):
        if self.updateValue != 'none':
        
            col = int(round(xval / 32))
            row = int(round(yval / 32))
            
            if row == 0 or row == 1:
            
                if col == 0 or col == 1:
                    print '1'
                    self.newValue *= 10
                    self.newValue += 1
                if col == 2 or col == 3:
                    print '2'
                    self.newValue *= 10
                    self.newValue += 2
                if col == 4 or col == 5:
                    print '3'
                    self.newValue *= 10
                    self.newValue += 3
                    
                if col == 6 or col == 7 or col == 8:
                    print 'enter'
                    
                    if self.self.updateValue == 'number':
                        if self.newValue > 127:
                            self.updateValue = 'none'
                            self.newValue = 0
                        else:
                            self.ccNumbers[self.updatecc] = self.newValue
                            data = [self.updateValue + 1, self.newValue]
                            __main__.sendOSCMessage('/curve/track/edit/midi_params/cc_number', data)
                            
                    elif self.updateValue == 'length':
                        if self.newValue < 1 or self.newValue > 16:
                            self.updateValue = 'none'
                            self.newValue = 0
                        else:
                            self.ccLengths[self.updatecc] = self.newValue
                            data = [self.newValue]
                            __main__.sendOSCMessage('/curve/track/edit/curve_length', data)
                            
                    elif self.updateValue == 'channel':
                        if self.newValue > 15:
                            self.updateValue = 'none'
                            self.newValue = 0
                        else:
                            self.ccChannel[self.updatecc] = self.newValue
                            data = [self.newValue]
                            __main__.sendOSCMessage('/curve/track/edit/midi_params/midi_channel', data)
                    self.updateValue = 'none'
                    self.newValue = 0
                    
            if row == 2 or row == 3:
            
                if col == 0 or col == 1:
                    print '4'
                    self.newValue *= 10
                    self.newValue += 4
                if col == 2 or col == 3:
                    print '5'
                    self.newValue *= 10
                    self.newValue += 5
                if col == 4 or col == 5:
                    print '6'
                    self.newValue *= 10
                    self.newValue += 6
                if col == 6 or col == 7 or col == 8:
                    print 'cancel'
                    self.updateValue = 'none'
                    self.newValue = 0
                    
            if row == 4 or row == 5:
            
                if col == 0 or col == 1:
                    print '7'
                    self.newValue *= 10
                    self.newValue += 7
                if col == 2 or col == 3:
                    print '8'
                    self.newValue *= 10
                    self.newValue += 8
                if col == 4 or col == 5:
                    print '9'
                    self.newValue *= 10
                    self.newValue += 9
                if col == 6 or col == 7:
                    print '0'
                    self.newValue *= 10


    def inputOptionsScreen(self, pos):
        col = int(round(pos[0] / 64))
        row = int(round(pos[1] / 64))
        if row > 7:
            self.navButtonInterface(col)
            self.updateValue = 'none'
        else:
            self.inputMidiOptions(pos)

