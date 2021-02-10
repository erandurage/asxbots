import threading
import time
import random
class Consumer:
    def __init__(self, seccode, syncgroup):
        self.cv = threading.Condition()
        self.data = []
        self.seccode = seccode
        self.i = 1
        self.p = 0
        self.security_group = syncgroup
    
    def consume(self, localdata):
        waitTime = random.random()
        time.sleep(waitTime)
        while len(localdata) > 0:
            p = localdata.pop(0)
            print(p)
        
    def run(self, dummy):
        while True:
            if self.security_group.flag.get() == 2:
                print("Consumer paused. Set flag to 0 to resume")
                time.sleep(1)
                continue
            
            localdata = []
            with self.cv:
                self.cv.wait()
                while len(self.data) > 0:
                    localdata.append(self.data.pop(0))
                    
            self.consume(localdata)
