import time
import random

from BrowserWindow import BrowserWindow
from CommSecDefs import CommSec
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from CommonDefs import Fields
from Password import *
from CommSecDefs import CommSec
import pandas as pd
import numpy as np
PRICE_MUL_FACTOR = 1000000
import datetime 
from scipy.signal import argrelextrema
seclist = [ 'PRL']
# seclist = ["RAN", "AVZ", "ECS", "VMS", "ANA", "MLX", "BMN", "VAL", "ASN", "EM1", "HCH", "IPT", "BGL", "MNS", "CRL", "ADO", "VIC", "EFE", "SHE", "PEN", "CAD", "DOU", "IBX", "ACW", "MGT", "TSC", "BCN", "PRM", "HSC", "ADV", "AGE", "MHC", "MSR", "AUZ", "RBR", "SRZ", "NPM", "GGG", "FPL", "NWE", "LKE", "MBK", "RFX", "BOE", "AGY", "SVL", "PDN", "PCL", "GGX", "ELT", "NTU", "CXO", "BUY", "QFY", "FRX", "CCA", "ICI", "DCC", "MCT", "VML", "AO1", "BRK", "HWK", "GTG", "GMR", "SYA", "LSR", "AOA", "HLX", "RNU", "SI6", "VPR", "IOU", "DW8", "IXR", "SRN", "ASP", "SCU", "LRS", "BPH", "CGB", "ARE", "ESH", "OEX", "ROG", "ANL", "QPM", "OAR", "CM8", "ANW", "9SP", "T3D", "MAY", "CLZ", "GLV", "CCE", "PUR", "SHO", "FGO", "ADX", "MXC", "XST", "JAT", "PWN", "88E", "WOO", "CRO", "FFG", "UUV", "PRL", "CI1"]
# seclist = [ "ADX", "MXC", "XST", "JAT", "PWN", "88E", "WOO", "CRO", "FFG", "UUV", "PRL", "CI1"]

# pd.options.display.float_format = '{:.2f}'.format
# browser = BrowserWindow(headless=False)
# browser.openURL(CommSec.HOME_URL)
# browser.createAction(CommSec.CLIENT_ID).send_keys(COMMSEC_USERNAME).send_keys(Keys.TAB)
# browser.createAction(CommSec.PASSWORD).send_keys(COMMSEC_PASSWORD).send_keys(Keys.RETURN)
# print(browser.createAction(CommSec.ACCOUNT_DETAILS).get_text())
#  
# for seccode in seclist:
#     print(seccode)
#     browser.openTab(CommSec.SECURITY_PARTIAL_URL.replace('___', seccode))
#     browser.switchToTab(1)
#     browser.createAction(CommSec.COURSE_OF_SALES).click()
#     browser.createAction(CommSec.DOWNLOAD_CSV).click()
#     time.sleep(1)
#     browser.closeCurrentTab()
#  
# time.sleep(5)
# browser.close()
totpnl = 0
dfasec = pd.DataFrame({"seccode":[], "trades":[]})
for seccode in seclist:
    print("Processing " + seccode)
    filename = 'Course_of_sales_'+ seccode +'_23Feb2021.csv'
    df = pd.DataFrame({'Time': [], "Price": [] })
    with open(filename) as f:
        lines = f.readlines()
        for line in reversed(lines[1:]):
            al = line.split(',')
            dfl = pd.DataFrame({'Time': [al[0]], "Price": [ np.float128(al[1])*PRICE_MUL_FACTOR] })
            dfl['Time'] = pd.to_datetime(dfl['Time'])
            df = df.append(dfl)
            df.index = range(1,len(df)+1) 
            ma = df.rolling(window=20).mean()
            df['ma_Price'] = ma['Price']
            n = 20
            df['min'] = df.iloc[argrelextrema(df.ma_Price.values, np.less_equal, order=n)[0]]['ma_Price']
            df['max'] = df.iloc[argrelextrema(df.ma_Price.values, np.greater_equal,order=n)[0]]['ma_Price']
             
            df['minu'] = np.where(df['min']!=df['max'], df['min'], np.NaN)
            df['maxu'] = np.where(df['min']!=df['max'], df['max'], np.NaN)
            last = df.tail(1)
            if len(last.index):
                tgval =  (last)['minu'].iloc[0]
                if np.isnan(tgval) == False:
                    print("Buy at " + str(tgval))
#                     print(df)
#                     time.sleep(1000)
#             df = df.rename(columns={"Price $": "Price", "Value $": "Value"}).iloc[::-1]
    print(df.head(200).to_string())
        
#     df = pd.read_csv(filename)
#     
#     df = df[df['Time'] < datetime.datetime(2021, 2, 23, 10,30,0)]
# 
#     df = df.rename(columns={"Price $": "Price", "Value $": "Value"}).iloc[::-1]
#     df = df.drop(columns=['Market', 'Condition','Value', 'Volume'])
#     df.index = range(1,len(df)+1) 
#     df['Price'] = df['Price'] * PRICE_MUL_FACTOR
#     ma = df.rolling(window=20).mean()
#     df['ma_Price'] = ma['Price']
#     n = 20
#     df['min'] = df.iloc[argrelextrema(df.ma_Price.values, np.less_equal, order=n)[0]]['ma_Price']
#     df['max'] = df.iloc[argrelextrema(df.ma_Price.values, np.greater_equal,order=n)[0]]['ma_Price']
#     
#     df['minu'] = np.where(df['min']!=df['max'], df['min'], np.NaN)
#     df['maxu'] = np.where(df['min']!=df['max'], df['max'], np.NaN)
# 
# 
# #     print(df.to_string())
#     df.to_csv("calc.csv")
#     ma = df.rolling(window=20).mean()
#     madiff = ma.diff()
#     madiffma = madiff.rolling(window=20).mean()
#     df['ma_Price'] = ma['Price']
#     df['ma_Price_diff'] = madiff['Price']
#     df['ma_Price_diff_ma'] = madiffma['Price']
#     df['ma_Price_diff_ma_diff'] = madiffma.diff()['Price']
    
#     dfasec = dfasec.append(pd.DataFrame({"seccode":[seccode], "trades":[len(df.index)]}))
    
#     print(seccode + " ->" + str( len(df.index)))
# print(dfasec.sort_values(by=['trades']).to_string())
print("DONE")
    