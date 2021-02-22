from Number import Number
from CommonDefs import Fields
class OrderBookSide:
    def __init__(self):
        self.qty = []
        self.price = []
    
    def fill(self, qty, price):
        for q in qty:
            self.qty.append(Number(q).value)
        
        for p in price:
            self.price.append(Number(p).value)
    
    
    def getWeightedQty(self, weights):
        i = 0
        total = 0
        for w in weights:
            total = total + self.qty[i]*w
            
        return total
    
class OrderBook:
    def __init__(self, obdata):
        self.buy = OrderBookSide()
        self.sell = OrderBookSide()
        if len(obdata[Fields.BUYSIDE_PRICE]) != len(obdata[Fields.BUYSIDE_QTY]):
            raise ValueError("Buyers price array length does not match with buyers qty array length")
        
        self.buy.fill(obdata[Fields.BUYSIDE_QTY], obdata[Fields.BUYSIDE_PRICE])
        
        if len(obdata[Fields.SELLSIDE_PRICE]) != len(obdata[Fields.SELLSIDE_QTY]):
            raise ValueError("Sellers price array length does not match with sellers qty array length")
        
        self.sell.fill(obdata[Fields.SELLSIDE_QTY], obdata[Fields.SELLSIDE_PRICE])
        