import RPi.GPIO as GPIO  
import os
import threading
from pprint import pprint
from time import sleep
from threading import Thread
from WebWeather import WebWeather
from WebNews import WebNews

class GPIOHandler():
    threadLock = threading.Lock()
    rc = None
    currentVolume = 80
    # 0 = Not Shifted
    # 1 = Mega Shift
    # 2 = Ultra Shift
    # 3 = Monster Shift
    currentShiftLevel = 0    
    _PLAY = 17
    _PREV = 27
    _NEXT = 18
    _SHIFT = 22

    def __init__(self, rc1): 
        self.rc = rc1 

        GPIO.setmode(GPIO.BCM)
        # Play
        GPIO.setup(self._PLAY, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
        # Prev
        GPIO.setup(self._PREV, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
        # Next
        GPIO.setup(self._NEXT, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
        # Shift       
        GPIO.setup(self._SHIFT, GPIO.IN, pull_up_down=GPIO.PUD_UP)  

        GPIO.add_event_detect(self._PLAY, GPIO.FALLING, callback=self.Button_Logic, bouncetime=100)  
        GPIO.add_event_detect(self._PREV, GPIO.FALLING, callback=self.Button_Logic, bouncetime=100) 
        GPIO.add_event_detect(self._NEXT, GPIO.FALLING, callback=self.Button_Logic, bouncetime=100)  
        
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
        if self.currentShiftLevel == 0:
            # Level 0
            os.system("omxplayer --vol -1204 /home/pi/sounds/Down.m4a")
        elif self.currentShiftLevel == 1:
            # Level 1
            os.system("omxplayer --vol -1204  /home/pi/sounds/Up.m4a")
        if needUnPause:
            self.rc.UnPause()

    def Shift(self, direction):   
        print("Shift {}".format(direction))
        self.currentShiftLevel += direction
        if self.currentShiftLevel < 0:
            self.currentShiftLevel = 0            
        elif self.currentShiftLevel > 1: 
            self.currentShiftLevel = 1
        self.PlayShiftStatus()

    def Level0_NotShifted_Logic(self, channel):   
        if channel == self._PLAY:
            self.rc.Play()    
        elif channel == self._PREV:
            self.rc.Prev()    
        elif channel == self._NEXT:
            self.rc.Next()    
        self.threadLock.release()

    def Level0_Shifted_Logic(self, channel):   
        if channel == self._PLAY:
            self.Shift(1)  
        elif channel == self._PREV:
            # Volume Down 
            self.SetVolume(-5)  
        elif channel == self._NEXT:
            # Volume Up
            self.SetVolume(5) 
        self.threadLock.release()

    def Level1_NotShifted_Logic(self, channel):   
        if channel == self._PLAY:            
            self.Shift(-1)
        elif channel == self._PREV:
            # Change Genre Down            
            self.rc.PrevGenre()
        elif channel == self._NEXT:
            # Change Genre Up
            self.rc.NextGenre()
        self.threadLock.release()
    
    def Level1_Shifted_Logic(self, channel):   
        if channel == self._PLAY:            
            # Shutdown
            self.Finish()
            self.ShutDown()
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
            needUnPause = False
            if self.rc.ACTIVELY_PLAYING and not self.rc.PAUSED:
                needUnPause = True
                self.rc.Pause()
            w = WebNews()
            w.GO()        
            if needUnPause:
                self.rc.UnPause()   
        self.threadLock.release()          

    def Button_Logic(self, channel):  
        # Wait
        sleep(0.033)                 
        if GPIO.input(channel) == 0 and self.threadLock.acquire() == 1: 
            print("Button_Logic Start {}".format(self.currentShiftLevel))  

            if GPIO.input(self._SHIFT) == 0:
                # Shift is pressed
                if self.currentShiftLevel == 0:
                    # Level 0
                    Thread(target = self.Level0_Shifted_Logic(channel)).start()  
                else:
                    # Level 1
                    Thread(target = self.Level1_Shifted_Logic(channel)).start()                    
            else:
                # Shift is NOT pressed
                if self.currentShiftLevel == 0:
                    # Level 0
                    Thread(target = self.Level0_NotShifted_Logic(channel)).start()
                else:
                    # Level 1
                    Thread(target = self.Level1_NotShifted_Logic(channel)).start()
            print("Button_Logic Stop {}".format(self.currentShiftLevel))  
