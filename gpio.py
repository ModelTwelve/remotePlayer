import RPi.GPIO as GPIO  

class GPIOHandler():
    rc = None

    def __init__(self, rc1): 
        self.rc = rc1 

        GPIO.setmode(GPIO.BCM)
        # Play
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
        # Prev
        GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
        # Next
        GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
        # Stop/Init        
        GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)  

        GPIO.add_event_detect(17, GPIO.FALLING, callback=self.CallBack_Play, bouncetime=300)  
        GPIO.add_event_detect(27, GPIO.FALLING, callback=self.CallBack_Prev, bouncetime=300) 
        GPIO.add_event_detect(18, GPIO.FALLING, callback=self.CallBack_Next, bouncetime=300)  
        GPIO.add_event_detect(22, GPIO.FALLING, callback=self.CallBack_StopInit, bouncetime=300) 

    def Finish(self):
        GPIO.cleanup()             

    def CallBack_Play(self, channel):  
        self.rc.Play()        
    def CallBack_Prev(self, channel):  
        self.rc.Prev()
    def CallBack_Next(self, channel):  
        self.rc.Next()
    def CallBack_StopInit(self, channel):  
        self.rc.Stop()
        self.rc.InitList()
