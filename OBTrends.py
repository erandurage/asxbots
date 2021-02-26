import time
import random

from datetime import datetime
from BrowserWindow import BrowserWindow
from CommSecDefs import CommSec
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from CommonDefs import Fields
from Password import *
from CommSecDefs import CommSec
import pandas as pd
import numpy as np
from test import test_selectors
PRICE_MUL_FACTOR = 1000000
import datetime 
from scipy.signal import argrelextrema
from Atomic import AtomicDictionary
import threading
from pathlib import Path
import os 

def calcBuySide(dfnew, dfold, side):
    otherside = ''
    if side == 'B':
        otherside = 'S'
    elif side == 'S':
        otherside = 'B'
    else:
        raise ValueError("Invalid side " + side)
    
    dfnew = dfnew.drop(columns=[otherside+'C', otherside+'U',otherside+'P'])
    

    
    dfold[side + 'Pp'] = dfold[side + 'P']
    dfnew[side + 'Pd'] = dfnew[side + 'P']
    
    dfold = dfold.set_index(side + 'P')
    dfnew = dfnew.set_index(side + 'P')
    
    
    dfnew[side + 'Pp'] = dfold[side + 'Pp']
    dfnew[side + 'Up'] = dfold[side + 'U']
    dfnew[side + 'Cp'] = dfold[side + 'C']
    
    is_NaN = dfnew.isnull()
    row_has_NaN = is_NaN.any(axis=1)
    rows_with_NaN = dfnew[row_has_NaN]
    print(rows_with_NaN['Level'])
    print(dfnew)
    dfnew = dfnew.fillna(0)
     
    dfnew[side + 'Vd'] = dfnew[side + 'Pd']* dfnew[side + 'U']
    dfnew[side + 'Vp'] = dfnew[side + 'Pp']* dfnew[side + 'Up']
    dfnew[side + 'Vdiff'] = dfnew[side + 'Vd'] - dfnew[side + 'Vp']
    dfnew[side + 'Cdiff'] = dfnew[side + 'C'] - dfnew[side + 'Cp']
    
    weight_start = 1.6
    weight_step = 0.1
    weights = []
    for i in range(0, 16):
        weights.append(weight_start - i*weight_step)
    dfnew['w'] = weights
    
    dfnew[side + 'w'] = dfnew[side + 'Vdiff']* dfnew[side + 'Cdiff'] * dfnew['w']
    print(dfnew.to_string())
    return dfnew[side + 'w'].sum()

df1 = pd.read_csv("ob1.csv")
df2 = pd.read_csv("ob2.csv")

print(calcBuySide(df2, df1, 'B'))
print(calcBuySide(df2, df1, 'S'))

