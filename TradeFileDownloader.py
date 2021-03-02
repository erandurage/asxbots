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

pd.set_option('display.float_format', lambda x: '%.12f' % x)
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
# totpnl = 0
# dfasec = pd.DataFrame({"seccode":[], "trades":[]})
# for seccode in seclist:
#     print("Processing " + seccode)
#     filename = 'Course_of_sales_'+ seccode +'_23Feb2021.csv'
#     df = pd.DataFrame({'Time': [], "Price": [] })
#     with open(filename) as f:
#         lines = f.readlines()
#         for line in reversed(lines[1:]):
#             al = line.split(',')
#             dfl = pd.DataFrame({'Time': [al[0]], "Price": [ np.float128(al[1])*PRICE_MUL_FACTOR] })
#             dfl['Time'] = pd.to_datetime(dfl['Time'])
#             df = df.append(dfl)
#             df.index = range(1,len(df)+1) 
#             ma = df.rolling(window=20).mean()
#             df['ma_Price'] = ma['Price']
#             n = 20
#             df['min'] = df.iloc[argrelextrema(df.ma_Price.values, np.less_equal, order=n)[0]]['ma_Price']
#             df['max'] = df.iloc[argrelextrema(df.ma_Price.values, np.greater_equal,order=n)[0]]['ma_Price']
#              
#             df['minu'] = np.where(df['min']!=df['max'], df['min'], np.NaN)
#             df['maxu'] = np.where(df['min']!=df['max'], df['max'], np.NaN)
#             last = df.tail(1)
#             if len(last.index):
#                 tgval =  (last)['minu'].iloc[0]
#                 if np.isnan(tgval) == False:
#                     print("Buy at " + str(tgval))
# #                     print(df)
# #                     time.sleep(1000)
# #             df = df.rename(columns={"Price $": "Price", "Value $": "Value"}).iloc[::-1]
#     print(df.head(200).to_string())
        
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
# print("DONE")

selected_sec_data = AtomicDictionary()
selected_sec_data.set('df', pd.DataFrame())

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
    

    deln = 0
    for index, row in dfnew[::-1].iterrows():
        if np.isnan(row[side + 'Pp']) != True:
            break
        deln += 1
        
    
    is_NaN = dfnew.isnull()
    row_has_NaN = is_NaN.any(axis=1)
    rows_with_NaN = dfnew[row_has_NaN]

    dfnew = dfnew.fillna(0)

    dfnew.to_csv("out_data.csv")
    dfnew[side + 'Vd'] = dfnew[side + 'Pd']* dfnew[side + 'U']
    dfnew[side + 'Vp'] = dfnew[side + 'Pp']* dfnew[side + 'Up']
    dfnew[side + 'Vdiff'] = dfnew[side + 'Vd'] - dfnew[side + 'Vp']
    dfnew[side + 'Cdiff'] = dfnew[side + 'C'] - dfnew[side + 'Cp']
    
    weight_start = 1.6
    weight_step = 0.1
    weights = []
    for i in range(0, len(dfnew.index)):
        weights.append(weight_start - i*weight_step)
    dfnew['w'] = weights
    
    dfnew[side + 'w'] = dfnew[side + 'Vdiff']* dfnew[side + 'Cdiff'] * dfnew['w']


    dfnew.drop(dfnew.tail(deln).index, inplace = True) 
    return dfnew[side + 'w'].sum()

class CommSecExtractor:        
    def getOBSideSummary(self,str):
        astr = str.split('for')
        return astr[0].split()[0].strip().replace(',',''), astr[1].split()[0].strip().replace(',','')
    def _run(self, rundata):
        for sec in rundata['stocks']:
            secdata = rundata['stocks'][sec]['ad']
            secdata.set('ts', datetime.datetime.now().isoformat())
            
            time.sleep(1)
            
        
        print("Dummy extraction closed")
        
    def run(self, rundata):
        browser = browser = BrowserWindow(headless=True)
        browser.openURL(CommSec.HOME_URL)
        browser.createAction(CommSec.CLIENT_ID).send_keys(COMMSEC_USERNAME).send_keys(Keys.TAB)
        browser.createAction(CommSec.PASSWORD).send_keys(COMMSEC_PASSWORD).send_keys(Keys.RETURN)
        print(browser.createAction(CommSec.ACCOUNT_DETAILS).get_text())
        
        thread_local_data = {}
        
        while True:

            for sec in rundata['stocks']:
                if sec not in thread_local_data:
                    thread_local_data[sec] = {'obold': None, 'obnew': None}
#                 print("Doing work for " + sec)
                browser.openTab(CommSec.SECURITY_PARTIAL_URL.replace('___', sec))
                browser.switchToTab(1)
            
                if 'Error' in browser.getTitle():
                    browser.closeCurrentTab()
                    continue
            
                
                lastprice = ((browser.createAction(CommSec.LAST_PRICE).get_text().split('<'))[0]).strip().replace('$', '').replace(',', '').replace('-', '0')
                tradevalue = 0
                openprice = 0
                hightprice = 0
                lowprice = 0 
                bbprice = 0
                bsprice = 0
                buyercount = 0
                buyerunits = 0
                sellercount = 0
                sellerunits = 0
                
                items = browser.createAction(CommSec.STOCK_DETAILS_ITEM_SINGLE_FIELD)._find_all()
                for i in range(0, len(items)):
                    ih = items[i].get_attribute('innerHTML')
                    soup = BeautifulSoup(ih, 'html.parser')
                    soup.tooltip.span.span.span.next_sibling.clear()
                    fieldname = soup.tooltip.get_text()
                    value = soup.span.next_sibling.get_text()
                    if value == '-':
                        value = '0'
                    
                    value = value.replace(',', '')

                    if fieldname == 'Trades':
                        tradevalue = int(value) 
         
                items = browser.createAction(CommSec.STOCK_DETAILS_ITEM)._find_all()
                
                for i in range(0, len(items)):
                    ih = items[i].get_attribute('innerHTML')
                    soup = BeautifulSoup(ih, 'html.parser')
                    soup.span.tooltip.span.span.span.next_sibling.clear()
                    name = soup.span.get_text()
                    value = soup.span.next_sibling.get_text()
                     
                    if '/' in name:
                        ns = name.split('/')
                        vs = value.split('/')
                        
                        name = ns[0].strip()
                        value = vs[0].strip().replace(',','').replace('-', '0').replace('$', '')
                        if name == 'Bid':
                            bbprice = np.float64(value)
                        elif name == 'Offer':
                            bsprice = np.float64(value)
                            
                    else:
                        value = value.strip().replace(',','').replace('-', '0').replace('$', '')
                        if name == 'Open':
                            openprice = np.float64(value)
                        elif name == 'High':
                            hightprice = np.float64(value)
                        elif name == 'Low':
                            lowprice = np.float64(value)

                if bbprice > 0:
                    buyercount, buyerunits = self.getOBSideSummary(browser.createAction(CommSec.MD_SUMMARY_BUYERS).get_text())

                if bsprice > 0:
                    sellercount, sellerunits = self.getOBSideSummary(browser.createAction(CommSec.MD_SUMMARY_SELLERS).get_text())

                df = pd.DataFrame({'Timestamp':[datetime.datetime.now().isoformat()], 
                                   'Buyers_count':[buyercount], 
                                   'Buyers_units':[buyerunits], 
                                   'Sellers_count':[sellercount], 
                                   'Sellers_units':[sellerunits], 
                                   'Trades': [tradevalue],
                                   'Seccode': [sec],
                                   'Last':[lastprice],
                                   'Open':[openprice],
                                   'High':[hightprice],
                                   'Low':[lowprice]  
                                 })
                                
                df = df.set_index('Timestamp')
                df.index = pd.to_datetime(df.index)
                
                items = browser.createAction(CommSec.ORDER_BOOK)._find_all()
                hasOBLevels = False
                curOB = pd.DataFrame()
                obls = []
                for i in range(0, len(items)):
                    ih = items[i].get_attribute('innerHTML')
                    soup = BeautifulSoup(ih, 'html.parser')
                    tds = soup.find_all('td')
                    dfobl = pd.DataFrame()
                    dfobl =  dfobl.append(df)
                    dfobl['Level'] = i
                    dfobl['BC'] = np.float64(tds[0].get_text().strip().replace(',','').replace('-', '0').replace('$', ''))
                    dfobl['BU'] = np.float64(tds[1].get_text().strip().replace(',','').replace('-', '0').replace('$', ''))
                    dfobl['BP'] = np.float64(tds[2].get_text().strip().replace(',','').replace('-', '0').replace('$', ''))
                    dfobl['SC'] = np.float64(tds[5].get_text().strip().replace(',','').replace('-', '0').replace('$', ''))
                    dfobl['SU'] = np.float64(tds[4].get_text().strip().replace(',','').replace('-', '0').replace('$', ''))
                    dfobl['SP'] = np.float64(tds[3].get_text().strip().replace(',','').replace('-', '0').replace('$', ''))

#                     with selected_sec_data._lock:#POSSIBLE DEADLOCK
#                         selected_sec_data._value['df'] = selected_sec_data._value['df'].append(dfobl)
                    obls.append(dfobl)
                    curOB = curOB.append(dfobl, ignore_index=True)
                    hasOBLevels = True
                    
                

                        
                if hasOBLevels == False:
                    with selected_sec_data._lock:
                        selected_sec_data._value['df'] = selected_sec_data._value['df'].append(df)
                else:
                    curOB = curOB.drop(columns=['Level','Buyers_count', 'Buyers_units', 'Sellers_count', 'Sellers_units', 'Trades', 'Seccode', 'Last', 'Open', 'High', 'Low'])
#                     print(curOB)
                        
                    thread_local_data[sec]['obold'] = thread_local_data[sec]['obnew']
                    thread_local_data[sec]['obnew'] = pd.DataFrame().append(curOB)
                     
                    if thread_local_data[sec]['obold'] is not None:
                        buyweight = calcBuySide(thread_local_data[sec]['obnew'], thread_local_data[sec]['obold'], 'B')
                        sellweight = calcBuySide(thread_local_data[sec]['obnew'], thread_local_data[sec]['obold'], 'S')
                        

                        with selected_sec_data._lock:
#                             for dfobl in obls:
                            df['BuySideWeight'] = buyweight
                            df['SellSideWeight'] = sellweight
                            df['BuySellWeightDiff'] = buyweight - sellweight
                            selected_sec_data._value['df'] = selected_sec_data._value['df'].append(df)
                            
#                         print(selected_sec_data)
#                     outfilename = 'price_out_' + sec + ".csv"
#                     rundata['stocks'][sec]['dtstore'].orderbook_data.to_csv(outfilename)
                    
                
#                 if tradevalue > 0:
#                     browser.createAction(CommSec.COURSE_OF_SALES).click()
#                     browser.createAction(CommSec.DOWNLOAD_TRADES).click()
                browser.closeCurrentTab()
            time.sleep(2)
        browser.close()
        
class StockDataStore:
    def __init__(self):
        self.orderbook_data = pd.DataFrame({'Timestamp':[], 'Buyers_count':[], 'Buyers_units':[], 'Sellers_count':[], 'Sellers_units':[], 'Trades': [] })
        self.trade_data = pd.DataFrame({'Timestamp':[], 'Price':[], 'Volume':[]})
        
class DataLoader:
    def run(self, rundata):
        while True:
            
            for sec in rundata['stocks']:
            
                while True:
                    secdata = rundata['stocks'][sec]['ad']
                    
                    now = datetime.datetime.now()
                    filename = "Course_of_sales_"+  sec +"_"+ now.strftime("%d%b%Y") +".csv" 
                    fillfilepath = filename
                    my_file = Path(fillfilepath)
                    if my_file.is_file() != False:
    
                        df = pd.read_csv(filename)
                        os.remove(filename)
                        df = df.rename(columns={"Price $": "Price", 'Time': 'Timestamp'}).iloc[::-1]
                        df['Timestamp'] = pd.to_datetime(df['Timestamp']).dt.strftime('%Y-%m-%dT%H:%M%:%SZ')
                        df = df.drop(columns=['Market', 'Condition','Value $'])
#                         df.index = range(1,len(df)+1) 
                        df['Price'] = df['Price'] * PRICE_MUL_FACTOR
                        rundata['stocks'][sec]['dtstore'].trade_data = df
                        
                        outfilename = 'trades_out_' + sec + ".csv"
                        df.to_csv(outfilename)
                        break
                    
                    else:
                        time.sleep(2)
                
            time.sleep(10)
            
class ThreadGroup:
    def __init__(self, worker_key, thread_prefix='Th'):
        self.worker_key = worker_key
        self.thread_prefix = thread_prefix
        self.threads = []
        
    def wait_for_all(self):
        jc = 0
        stop = False
        while True:
            if stop == True:
                break
             
            for t in self.threads:
                t.join(3)
                if t.is_alive() == False:
                    jc = jc + 1
                    if jc == len(rundata):
                        print("All good")
                        stop = True
                        break 
                    
    def run(self, rundata):
        i = 0 
        for rd in rundata:
            cs = rd[self.worker_key]
            t = threading.Thread(name=self.thread_prefix+'_'+str(i), target=cs.run, args=(rd,))
            self.threads.append(t)
            t.start()
            i = i + 1
             
        self.wait_for_all()

rundata = [
            {
                'csecex': CommSecExtractor(),
                'dtloader': DataLoader(),
                'stocks':{
                    'LRS': { 
                        'ad': AtomicDictionary({}),
                        'dtstore': StockDataStore()
                        
                           },
                    'EGR': { 
                        'ad': AtomicDictionary({}),
                        'dtstore': StockDataStore()
                           }
                }
            }
#             {   
#                 'csecex': CommSecExtractor(),
#                 'dtloader': DataLoader(),
# #                 'cv': threading.Condition(),
#                 'stocks':{
#                     'BPH': { 
#                         'ad': AtomicDictionary({'ts':'', 'bc':0, 'bu':0, 'sc':0, 'su':0}),
#                         'dtstore': StockDataStore()
#                         
#                            }, 
#                     'CRO': { 
#                         'ad': AtomicDictionary({'ts':'', 'bc':0, 'bu':0, 'sc':0, 'su':0}),
#                         'dtstore': StockDataStore()
#                            }
#                 }
#             }
          ]   
max_threads = 1
rundata_loaded = []
for i in range(0, max_threads):
    rundata_loaded.append(  {
                                'csecex': CommSecExtractor(),
                                'dtloader': DataLoader(),
                                'stocks':{}
                            })

i = 0
with open('ASX_all.csv') as f:
    lines = f.readlines()
    for line in lines:
        sec = line.split(',')[0]
        if sec in ['VPCDA', 'CHA', 'EZZ', 'AEB','HGON', 'BRV', 'BWRDB', 'BFCNA']:
            continue
        print(sec)
        value = { 
                    'ad': AtomicDictionary({}),
                    'dtstore': StockDataStore()
                }
        
        rundata_loaded[i%max_threads]['stocks'][sec] = value
        i = i + 1

print(rundata_loaded)


rundata = rundata_loaded

main_threads = []
 
print("Starting extractors...")
t = threading.Thread(name='Th_CommSecExtractors', target=ThreadGroup('csecex', 'Th_CommSecExtractor').run, args=(rundata,))
main_threads.append(t)
t.start()
 
# print("Starting loaders...")
# t = threading.Thread(name='Th_Loaders', target=ThreadGroup('dtloader', 'Th_DataLoader').run, args=(rundata,))
# main_threads.append(t)
# t.start()
 
jc = 0
stop = False

while True:
    if stop == True:
        break
      
    for t in main_threads:
        t.join(3)
        with selected_sec_data._lock:
            print(selected_sec_data._value['df'])
            selected_sec_data._value['df'] = pd.DataFrame()
#             selected_sec_data._value['df'].to_csv("all_data.csv")
            
        if t.is_alive() == False:
            jc = jc + 1
            if jc == 2:
                print("All good")
                stop = True
                break 

