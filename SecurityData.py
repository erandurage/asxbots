import hashlib
import time
import json
import copy
import pandas
import numpy
from Atomic import AtomicPrinter
globalAtomicPrinter = AtomicPrinter()
from CommonDefs import Fields
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
        self.BuySellRatio = []
        self.l1trendPrice = []
        self.finalTrendPrice = []
        
        self.BuySellRatioDiff = []
        self.l1trendPriceDiff = []
        self.finalTrendPriceDiff = []
        
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
        self.changes.append(diff)
        
        globalAtomicPrinter.printit(snapshot)
        
        # Business logic by chanaka....
        # Total quantity at the top level of orderbook
        l1Qty = float(snapshot["ORDERBOOK"]["BuySideQty"][0].replace(",", "")) + float(snapshot["ORDERBOOK"]["SellSideQty"][0].replace(",", ""))
        # Price difference between top level buy order and sell order
        l1Diff = float(snapshot["ORDERBOOK"]["SellSidePrice"][0].replace(",", "")) - float(snapshot["ORDERBOOK"]["BuySidePrice"][0].replace(",", ""))

        #Number of active buying quantity and selling quantity - first 6 levels considered and weight given for each level
        buyerAmt = float(snapshot["ORDERBOOK"]["BuySideQty"][0].replace(",", "")) + float(snapshot["ORDERBOOK"]["BuySideQty"][1].replace(",", "")) * .9 + float(snapshot["ORDERBOOK"]["BuySideQty"][2].replace(",", "")) * .8 + float(snapshot["ORDERBOOK"]["BuySideQty"][3].replace(",", ""))* .7 + float(snapshot["ORDERBOOK"]["BuySideQty"][4].replace(",", "")) * .6 + float(snapshot["ORDERBOOK"]["BuySideQty"][5].replace(",", "")) * .5
        sellerAmt = float(snapshot["ORDERBOOK"]["SellSideQty"][0].replace(",", "")) + float(snapshot["ORDERBOOK"]["SellSideQty"][1].replace(",", "")) * .9 + float(snapshot["ORDERBOOK"]["SellSideQty"][2].replace(",", "")) * .8 + float(snapshot["ORDERBOOK"]["SellSideQty"][3].replace(",", ""))* .7 + float(snapshot["ORDERBOOK"]["SellSideQty"][4].replace(",", "")) * .6 + float(snapshot["ORDERBOOK"]["SellSideQty"][5].replace(",", "")) * .5
        # Buy/Sell ratio based on above values - much better than whats shown in commsec webpage
        BuySellRatio = buyerAmt/sellerAmt

        # Trending price calculated based on top level - this is a virtual value ATM for the stock - much better than last traded price
        l1trendPrice = float(snapshot["ORDERBOOK"]["BuySidePrice"][0].replace(",", "")) + l1Diff * float(snapshot["ORDERBOOK"]["BuySideQty"][0].replace(",", "")) / l1Qty
        # Trending price calculated based on six levels - this is the final virtual value ATM for the stock 
        finalTrendPrice = float(snapshot["ORDERBOOK"]["BuySidePrice"][0].replace(",", "")) + l1Diff * buyerAmt / (buyerAmt + sellerAmt)
        
        # We need to remove this once debugging finished
        globalAtomicPrinter.printit(snapshot["ORDERBOOK"])
        
        #globalAtomicPrinter.printit("Buy Sell Ratio - " + str(BuySellRatio))
        #globalAtomicPrinter.printit("Level 1 Trend Price - " + str(l1trendPrice))
        #globalAtomicPrinter.printit("Final Trend Price - " + str(finalTrendPrice))
        
        # If at least one history values available, go and calculate differences
        if len(self.BuySellRatio) > 0 and len(self.l1trendPrice) and len(self.finalTrendPrice):
            # Calculate the change for each indicator
            BuySellRatioDiff = BuySellRatio - self.BuySellRatio[-1]
            l1TrendDiff = l1trendPrice - self.l1trendPrice[-1]
            FinalTrendDiff = finalTrendPrice - self.finalTrendPrice[-1]
            
            # Save these differences in self variables for the use of next iteration
            self.BuySellRatioDiff.append(BuySellRatioDiff)
            self.l1trendPriceDiff.append(l1TrendDiff)
            self.finalTrendPriceDiff.append(FinalTrendDiff)
        
        # Add calculated values for self variables for the use in next iteration
        self.BuySellRatio.append(BuySellRatio)
        self.l1trendPrice.append(l1trendPrice)
        self.finalTrendPrice.append(finalTrendPrice)
        
        # Define weight sequences for weighted average calculations
        ma_weights10 = [.1,.2,.3,.4,.5,.6,.7,.8,.9,1]
        ma_weights05 = [.2,.4,.6,.8,1]
        
        # Analyse trand and decide buying/ selling part starts here
        
        # Go inside and calculate trends when we have at least 10 history records
        if len(self.BuySellRatioDiff) > 9:
            # Calculate weighted average for all three indicators, for last 5 iterations and last 10 iterations
            wa_bs_ratio_diff10 = round(numpy.average( self.BuySellRatioDiff[-10:], weights = ma_weights10),2)
            wa_bs_ratio_diff05 = round(numpy.average( self.BuySellRatioDiff[-5:], weights = ma_weights05),2)
            
            wa_l1trend_diff10 = round(numpy.average( self.l1trendPriceDiff[-10:], weights = ma_weights10),2)
            wa_l1trend_diff05 = round(numpy.average( self.l1trendPriceDiff[-5:], weights = ma_weights05),2)    
            
            wa_finalTrend_diff10 = round(numpy.average( self.finalTrendPriceDiff[-10:], weights = ma_weights10),2)
            wa_finalTrend_diff05 = round(numpy.average( self.finalTrendPriceDiff[-5:], weights = ma_weights05),2)   
            
            # If all three indicators are positive and weighted average of last 5 is better than last 10, things are moving in right direction. Better buy it
            if (wa_bs_ratio_diff10 > 0 and wa_bs_ratio_diff05 > wa_bs_ratio_diff10 and wa_l1trend_diff10 > 0 and wa_l1trend_diff05 > wa_l1trend_diff10 and wa_finalTrend_diff10 > 0 and wa_finalTrend_diff05 > wa_finalTrend_diff10) :
                globalAtomicPrinter.printit("BUY IT, HURRY UP, Its going up.... Hooray.....  Stock - " +  snapshot["ORDERBOOK"]["EXCHANGE_CODE"] + "  Limit - " + snapshot["ORDERBOOK"]["BuySidePrice"][0] + "  Market - " + snapshot["ORDERBOOK"]["SellSidePrice"][0])
                
            # If all indicators are negative and weighted average of last 5 is worse than last 10, this one is going down. Better to sell and save our asses.    
            if(wa_bs_ratio_diff10 < 0 and wa_bs_ratio_diff05 < wa_bs_ratio_diff10 and wa_l1trend_diff10 < 0 and wa_l1trend_diff05 < wa_l1trend_diff10 and wa_finalTrend_diff10 < 0 and wa_finalTrend_diff05 < wa_finalTrend_diff10):
                globalAtomicPrinter.printit("SELL IT, HURRY UP, OMG Its going down.... :(.....  Stock - " +  snapshot["ORDERBOOK"]["EXCHANGE_CODE"] + "  Limit - " + snapshot["ORDERBOOK"]["SellSidePrice"][0] + "  Market - " + snapshot["ORDERBOOK"]["BuySidePrice"][0])
        
        # We can improve these indicators and include more indicators as we go on.
        # In addition we can identify more cases using these indicators, ATM we only track two definite going down or up scenarios. But this may be more than enough to make big $$$$ if we get indicators right. 
        
        #if len(diff) > 0:
        #    diff[Fields.EXCHANGE_CODE] = new[Fields.EXCHANGE_CODE]
        #    diff[Fields.SECURITY_CODE] = new[Fields.SECURITY_CODE]
        #    globalAtomicPrinter.printit(diff)
    
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


    
    
