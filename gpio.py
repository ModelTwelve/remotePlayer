import RPi.GPIO as GPIO  
import os
from time import sleep

class GPIOHandler():
    rc = None
    currentVolume = 80
    # 0 = Not Shifted
    # 1 = Shifted
    # 2 = Sticky Shifted
    # 3 = Super Shifted
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

        GPIO.add_event_detect(self._PLAY, GPIO.FALLING, callback=self.Button_Logic, bouncetime=300)  
        GPIO.add_event_detect(self._PREV, GPIO.FALLING, callback=self.Button_Logic, bouncetime=300) 
        GPIO.add_event_detect(self._NEXT, GPIO.FALLING, callback=self.Button_Logic, bouncetime=300)  
        GPIO.add_event_detect(self._STOP, GPIO.FALLING, callback=self.Button_Logic, bouncetime=300) 

        self.SetVolume()

    def Finish(self):
        GPIO.cleanup()
    
    def ShutDown(self):
        os.system("shutdown now")
    
    def SetVolume(self):
        os.system("amixer cset numid=1 {0}%".format(self.currentVolume))    

    def Button_Logic(self, channel):            
        if self.shiftStatus == 0:
            if channel == self._PLAY:
                self.rc.Play()    
            elif channel == self._PREV:
                self.rc.Prev()    
            elif channel == self._NEXT:
                self.rc.Next()    
            else: # channel == self._STOP:            
                # Set Shifted
                self.shiftStatus = 1  
        else:            
            if channel == self._STOP and self.shiftStatus == 1:            
                # Reset Shifted and Rest
                self.shiftStatus = 0
                self.rc.Stop()
                self.rc.InitList()     
            else:
                if channel == self._PLAY:
                    if self.shiftStatus == 1: 
                        # Set Super Shifted
                        self.shiftStatus = 3
                    elif self.shiftStatus == 3:
                        # Shutdown
                        self.Finish()
                        self.ShutDown()
                    else:
                        # Reset Shift
                        self.shiftStatus = 0
                elif channel == self._PREV:
                    # Set Sticky Shifted
                    self.shiftStatus = 2
                    self.currentVolume -= 5
                    self.SetVolume()  
                elif channel == self._NEXT:
                    # Set Sticky Shifted
                    self.shiftStatus = 2
                    self.currentVolume += 5
                    self.SetVolume()
                else:
                    # Stop
                    # Reset Shift
                    self.shiftStatus = 0
            
