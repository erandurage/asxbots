import time
import random

class Producer:
    def __init__(self, consumer_group, syncgroup):
        self.consumer_group = consumer_group
        self.security_group = syncgroup
        
    def produce(self, consumer):
        consumer.p = consumer.p + 1
        waitTime = random.random()
        time.sleep(waitTime)
        return str(consumer.p)
    
    def run(self, dummy):
        while True:
            if self.security_group.flag.get() == 1:
                print("Producer paused. Set flag to 0 to resume")
                time.sleep(1)
                continue
                
            for consumer in self.consumer_group:
                product = self.produce(consumer)

                with consumer.cv:
                    consumer.data.append(product)
                    consumer.cv.notifyAll()
            
