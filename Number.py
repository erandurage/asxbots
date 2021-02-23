from Atomic import AtomicPrinter
from ast import Num
globalAtomicPrinter = AtomicPrinter()
import numpy as np
class Number:
    def remove_dirty_strs(self, str):
        for sr in [",", "-", " ", "$"]:
            str = str.replace(sr, '')
        
        if str == '':
            str = '0'
            
        return str
    
    def __init__(self, str):
        str = self.remove_dirty_strs(str).strip()
        self.value = np.float128(str)
    