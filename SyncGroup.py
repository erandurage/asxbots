from Atomic import AtomicNumber
from Consumer import Consumer
from Producer import Producer
import threading
class SyncGroup:
    def __init__(self, securities):
        self.consumer_group = []
        for security in securities:
            self.consumer_group.append(Consumer(security, self))
            
        self.producer = Producer(self.consumer_group, self)
        self.flag = AtomicNumber()
        self.i = 0
        
    def timer(self):
        self.i = self.i + 1

        

                
    def run(self):
        threads = []
        for consumer in self.consumer_group:
            t = threading.Thread(name=consumer.seccode, target=consumer.run, args=(0,))
            threads.append(t)
            t.start()
        
        t = threading.Thread(name='producer', target=self.producer.run, args=(1,))
        threads.append(t)
        t.start()
        
        while True:
            for t in threads:
                t.join(3)
                self.timer()
