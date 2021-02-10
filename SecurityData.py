from SyncGroup import SyncGroup        
import hashlib
import time
import json
import copy
from Atomic import AtomicPrinter
globalAtomicPrinter = AtomicPrinter()

def getSHA512Hash(s):
    b = bytearray()
    b.extend(map(ord, s))
    hash_object = hashlib.sha512(b)
    return hash_object.hexdigest()

 
    
class SecurityData:
    def __init__(self):
        self.snapshot = {}
        self.history = []
        self.changes =[]
        
    def processUpdate(self, new):
        retdiff = {}
        snapshot = {}
        if getSHA512Hash(json.dumps(self.snapshot)) == getSHA512Hash(json.dumps(new)):
            print("No change")
            return
        
        for key1 in self.snapshot:
            snapshot[key1] = self.snapshot[key1]
            if key1 in new and key1 != 'OrderBook':
                if self.snapshot[key1] != new[key1]:
                    retdiff[key1] = new[key1]
        
        for key2 in new:
            snapshot[key2] = new[key2]
            if key2 not in self.snapshot and key2 != 'OrderBook':
                retdiff[key2] = new[key2]
        
    
        oldobhash = ''
        newobhash = ''
        
        if 'OrderBook' in self.snapshot:
            oldobhash = getSHA512Hash(json.dumps(self.snapshot['OrderBook']))
        if 'OrderBook' in new:
            newobhash =  getSHA512Hash(json.dumps(new['OrderBook']))
        
        if newobhash != oldobhash:
            retdiff['OrderBookChanges'] = True
        
        if len(self.snapshot) > 0:
            self.history.append(self.snapshot)
        self.snapshot = snapshot
        self.changes.append(retdiff)
        if len(retdiff) > 0:
            retdiff['Exchange'] = new['Exchange']
            retdiff['Security Code'] = new['Security Code']
            globalAtomicPrinter.printit(retdiff)
    
    def printData(self):
        print(json.dumps(self.snapshot, indent=2))
        print(json.dumps(self.history, indent=2))
        print(json.dumps(self.changes, indent=2))
        print("=============================")
    

        

if __name__ == '__main__':


    
#     sf = SyncGroup(['a', 'b', 'c'])
#     sf.run()
#   
    sd = SecurityData()  
    s1 = {
            'Exchange' : "ASX",
            'Security Code' : "BHP",
            'Last traded price': "12.87",
            'Last traded volume': "8272",
            'OrderBook': {
                'BuySidePrice': ["12.98", "12.96"]
            }
     }
    
    sd.processUpdate(s1)
#     sd.printData()

    s2 = {
            'Exchange' : "ASX",
            'Security Code' : "BHP",
            'Last traded price': "12.88",
            'Bid qty': "272",
            'OrderBook': {
                'BuySidePrice': ["13.05", "12.97", "12.96"]
            }
     }
    sd.processUpdate(s2)
#     sd.printData()
    s3 = {
            'Exchange' : "ASX",
            'Security Code' : "BHP",
            'Last traded price': "12.88",
            'Bid qty': "272",
            'OrderBook': {
                'BuySidePrice': ["13.05", "12.97", "12.963"]
            }
     }
    sd.processUpdate(s3)
#     sd.printData()


    
    
