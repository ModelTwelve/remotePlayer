import RPi.GPIO as GPIO  
import os
from pprint import pprint
from time import sleep
from threading import Thread
from WebWeather import WebWeather

class GPIOHandler():
    rc = None
    currentVolume = 80
    # 0 = Not Shifted
    # 1 = Mega Shift
    # 2 = Ultra Shift
    # 3 = Monster Shift
    shiftStatus = 0    
    _PLAY = 17
    _PREV = 27
    _NEXT = 18
    _STOP = 22

    def __init__(self, rc1): 
        self.rc = rc1 

        GPIO.setmode(GPIO.BCM)
        # Play
        GPIO.setup(self._PLAY, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
        # Prev
        GPIO.setup(self._PREV, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
        # Next
        GPIO.setup(self._NEXT, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
        # Stop/Init        
        GPIO.setup(self._STOP, GPIO.IN, pull_up_down=GPIO.PUD_UP)  

        GPIO.add_event_detect(self._PLAY, GPIO.FALLING, callback=self.Button_Logic, bouncetime=100)  
        GPIO.add_event_detect(self._PREV, GPIO.FALLING, callback=self.Button_Logic, bouncetime=100) 
        GPIO.add_event_detect(self._NEXT, GPIO.FALLING, callback=self.Button_Logic, bouncetime=100)  
        GPIO.add_event_detect(self._STOP, GPIO.FALLING, callback=self.Button_Logic, bouncetime=100) 

        self.SetVolume(0)

    def Finish(self):
        GPIO.cleanup()
    
    def ShutDown(self):
        os.system("shutdown now")
    
    def SetVolume(self, delta):
        self.currentVolume += delta
        os.system("amixer cset numid=1 {0}%".format(self.currentVolume)) 

    def PlayShiftStatus(self):
        needUnPause = False
        if self.rc.ACTIVELY_PLAYING and not self.rc.PAUSED:
            needUnPause = True
            self.rc.Pause()
        if self.shiftStatus == 0:
            # NotShifted
            os.system("omxplayer --vol -1204 /home/pi/sounds/NotShifted.m4a")
        elif self.shiftStatus == 1:
            # MegaShift
            os.system("omxplayer --vol -1204  /home/pi/sounds/MegaShift.m4a")
        elif self.shiftStatus == 2:
            # UltraShift
            os.system("omxplayer --vol -1204  /home/pi/sounds/UltraShift.m4a")
        elif self.shiftStatus == 3:
            # MonsterShift
            os.system("omxplayer --vol -1204  /home/pi/sounds/MonsterShift.m4a")
        if needUnPause:
            self.rc.UnPause()

    def Shift(self, direction):   
        print("Shift {}".format(direction))
        self.shiftStatus += direction
        if self.shiftStatus < 0:
            self.shiftStatus = 0            
        elif self.shiftStatus > 3: 
            self.shiftStatus = 3
        self.PlayShiftStatus()

    def NotShifted_Logic(self, channel):   
        if channel == self._PLAY:
            self.rc.Play()    
        elif channel == self._PREV:
            self.rc.Prev()    
        elif channel == self._NEXT:
            self.rc.Next()    
        elif channel == self._STOP:            
            # Set Mega Shift
            self.Shift(1)

    def MegaShift_Logic(self, channel):   
        if channel == self._PLAY:
            # Set Not Shifted
            self.Shift(-1)
        elif channel == self._PREV:
            # Volume Down 
            self.SetVolume(-5)  
        elif channel == self._NEXT:
            # Volume Up
            self.SetVolume(5)  
        elif channel == self._STOP:            
            # Set Ultra Shift
            self.Shift(1)

    def UltraShift_Logic(self, channel):   
        if channel == self._PLAY:
            # Set Mega Shift
            self.Shift(-1)
        elif channel == self._PREV:
            # Change Genre Down            
            self.rc.PrevGenre()
        elif channel == self._NEXT:
            # Change Genre Up
            self.rc.NextGenre()
        elif channel == self._STOP:            
            # Set Monster Shift
            self.Shift(1)

    def MonsterShift_Logic(self, channel):   
        if channel == self._PLAY:
            # Set Mega Shift
            self.Shift(-1)
        elif channel == self._PREV:
            # Web Call 1          
            needUnPause = False
            if self.rc.ACTIVELY_PLAYING and not self.rc.PAUSED:
                needUnPause = True
                self.rc.Pause()
            w = WebWeather()
            w.GO()        
            if needUnPause:
                self.rc.UnPause()    
        elif channel == self._NEXT:
            # Web Call 2
            pass
        elif channel == self._STOP:            
            # Shutdown
            self.Finish()
            self.ShutDown()

    def Button_Logic(self, channel):  
        # Wait
        sleep(0.033)                 
        if GPIO.input(channel) == 0:
            print("Button_Logic Start {}".format(self.shiftStatus))  
            if self.shiftStatus == 0:
                Thread(target = self.NotShifted_Logic(channel)).start()
            elif self.shiftStatus == 1:
                Thread(target = self.MegaShift_Logic(channel)).start()
            elif self.shiftStatus == 2:
                Thread(target = self.UltraShift_Logic(channel)).start()
            elif self.shiftStatus == 3:
                Thread(target = self.MonsterShift_Logic(channel)).start()
    
            print("Button_Logic Stop {}".format(self.shiftStatus))  
