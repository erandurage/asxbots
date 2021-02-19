import hashlib
import time
import json
import copy
from Atomic import AtomicPrinter
globalAtomicPrinter = AtomicPrinter()
from CommonDefs import Fields
import pandas as pd
import numpy as np

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
        self.trade_df = pd.DataFrame({Fields.LAST_PRICE: [],Fields.LAST_TRADED:[]})
    

    def processTrade(self, data):
        df = pd.DataFrame({Fields.LAST_PRICE: [ float(data[Fields.LAST_PRICE])],Fields.LAST_TRADED:[data[Fields.LAST_TRADED]]})
        self.trade_df = self.trade_df.append(df)
        self.trade_df['movav'] = self.trade_df.rolling(window=3).mean() 
        
    def processUpdate(self, new):
        diff = {}
        snapshot = {}
        if getSHA512Hash(json.dumps(self.snapshot)) == getSHA512Hash(json.dumps(new)):
#             print("No change")
            return
        
        
        for key1 in self.snapshot:
            snapshot[key1] = self.snapshot[key1]
            if key1 in new and key1 != Fields.ORDERBOOK:
                if self.snapshot[key1] != new[key1]:
                    diff[key1] = new[key1]
        
        for key2 in new:
            snapshot[key2] = new[key2]
            if key2 not in self.snapshot and key2 != Fields.ORDERBOOK:
                diff[key2] = new[key2]
        
    
        oldobhash = ''
        newobhash = ''
        
        if Fields.ORDERBOOK in self.snapshot:
            oldobhash = getSHA512Hash(json.dumps(self.snapshot[Fields.ORDERBOOK]))
        if Fields.ORDERBOOK in new:
            newobhash =  getSHA512Hash(json.dumps(new[Fields.ORDERBOOK]))
        
        if newobhash != oldobhash:
            diff['OrderBookChanges'] = True
        
        if len(self.snapshot) > 0:
            self.history.append(self.snapshot)
        self.snapshot = snapshot
        
        if Fields.LAST_TRADED in new and Fields.LAST_PRICE not in diff:
            diff[Fields.LAST_PRICE] = self.snapshot[Fields.LAST_PRICE]
            
        self.changes.append(diff)
        if Fields.LAST_PRICE in diff and Fields.LAST_TRADED in diff:
            self.processTrade(diff)
            globalAtomicPrinter.printit(diff)
            globalAtomicPrinter.printit(self.trade_df)
#         globalAtomicPrinter.printit(snapshot)
        if len(diff) > 0:
            diff[Fields.EXCHANGE_CODE] = new[Fields.EXCHANGE_CODE]
            diff[Fields.SECURITY_CODE] = new[Fields.SECURITY_CODE]
            globalAtomicPrinter.printit(diff)
    
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
            'Exchange Code' : "ASX",
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
            'Exchange Code' : "ASX",
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
            'Exchange Code' : "ASX",
            'Security Code' : "BHP",
            'Last traded price': "12.88",
            'Bid qty': "272",
            'OrderBook': {
                'BuySidePrice': ["13.05", "12.97", "12.963"]
            }
     }
    sd.processUpdate(s3)
#     sd.printData()


    
    
