import RPi.GPIO as GPIO  
import os

class GPIOHandler():
    rc = None
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

        GPIO.add_event_detect(self._PLAY, GPIO.FALLING, callback=self.CallBack_Play, bouncetime=300)  
        GPIO.add_event_detect(self._PREV, GPIO.FALLING, callback=self.CallBack_Prev, bouncetime=300) 
        GPIO.add_event_detect(self._NEXT, GPIO.FALLING, callback=self.CallBack_Next, bouncetime=300)  
        GPIO.add_event_detect(self._STOP, GPIO.FALLING, callback=self.CallBack_StopInit, bouncetime=300) 

    def Finish(self):
        GPIO.cleanup()             

    def CallBack_Play(self, channel):
        # Check GPIO 22 Stop/Init
        # If that button is also pushed then assume shutdown is requested instead
        if GPIO.input(self._STOP) == GPIO.LOW:
            os.system("shutdown now")      
        else:
            # Typical / expected
            self.rc.Play()        
    def CallBack_Prev(self, channel):  
        self.rc.Prev()
    def CallBack_Next(self, channel):  
        self.rc.Next()
    def CallBack_StopInit(self, channel):  
        self.rc.Stop()
        self.rc.InitList()
