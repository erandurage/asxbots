'''
Created on 3 Feb 2021

@author: Eran Rathnayake
'''



from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import traceback
import inspect
import time
import random
import threading, queue
import json
from bs4 import BeautifulSoup
from BrowserWindow import BrowserWindow
from CommSecDefs import CommSec

securities = ['ATH', 'XST', 'SCU', 'FRX', 'CCE', 'CAV', 'IXR', 'IOU', 'CRL', 'PWN', 'CLZ', 'UUV', 'BSM', 'AZI', 'SYA'] 
securities_per_thread = 4
update_queue = queue.Queue()
   
def extract_security_data(securities, dummy):
    print(securities)

    browser = BrowserWindow()
    browser.openURL(CommSec.HOME_URL)
    browser.createAction(CommSec.CLIENT_ID).send_keys('56352429').send_keys(Keys.TAB)
    browser.createAction(CommSec.PASSWORD).send_keys('Subotaei1!CSEC').send_keys(Keys.RETURN)
    print(browser.createAction(CommSec.ACCOUNT_DETAILS).get_text())

    for seccode in securities:      
        browser.openTab(CommSec.SECURITY_PARTIAL_URL.replace('___', seccode))
    
      
    while True:
        start = time.time()
        for wh in range(1, len(seccode)+1):
            browser.switchToTab(wh)
            stock_summary = {}
            stock_summary['Name'] = ((browser.createAction(CommSec.INSTRUMENT_DETAILS).get_text().split('<'))[0]).strip()
            stock_summary['Exchange Code'] = browser.createAction(CommSec.EXCHANGE_CODE).get_text()
            stock_summary['Security Code'] = browser.createAction(CommSec.SECURITY_CODE).get_text()
            stock_summary['Last price'] = ((browser.createAction(CommSec.LAST_PRICE).get_text().split('<'))[0]).strip()
            stock_summary['Todays Change'] = browser.createAction(CommSec.TODAYS_CHANGE_AMOUNT).get_text(1).strip()
    
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
                    if len(ns) != len(vs):
                        print("Multi value not found for all")
                    for i in range(0,len(ns)):
                        stock_summary[ns[i].strip()] = vs[i].strip()
                else:
                    stock_summary[name] = value
                     
            items = browser.createAction(CommSec.STOCK_DETAILS_ITEM_SINGLE_FIELD)._find_all()
            for i in range(0, len(items)):
                ih = items[i].get_attribute('innerHTML')
                soup = BeautifulSoup(ih, 'html.parser')
                soup.tooltip.span.span.span.next_sibling.clear()
                stock_summary[soup.tooltip.get_text()] = soup.span.next_sibling.get_text()
    
    
            for key in stock_summary:
                v = stock_summary[key]
                find_strs = ['$', '<!---->', ',']
                for fs in find_strs:
                    if fs in v:
                        v = v.replace(fs, '')
                 
                v = v.strip()
                stock_summary[key] = v
             
            stock_summary['OrderBook'] = {}
            stock_summary['OrderBook']['BuySideNumber'] = []
            stock_summary['OrderBook']['BuySideQty'] = []
            stock_summary['OrderBook']['BuySidePrice'] = [] 
            stock_summary['OrderBook']['SellSideNumber'] = []
            stock_summary['OrderBook']['SellSideQty'] = []
            stock_summary['OrderBook']['SellSidePrice'] = [] 
             
            items = browser.createAction(CommSec.ORDER_BOOK)._find_all()
            for i in range(0, len(items)):
                ih = items[i].get_attribute('innerHTML')
                soup = BeautifulSoup(ih, 'html.parser')
                tds = soup.find_all('td')
                stock_summary['OrderBook']['BuySideNumber'].append(tds[0].get_text())
                stock_summary['OrderBook']['BuySideQty'].append(tds[1].get_text())
                stock_summary['OrderBook']['BuySidePrice'].append(tds[2].get_text())
                stock_summary['OrderBook']['SellSideNumber'].append(tds[5].get_text())
                stock_summary['OrderBook']['SellSideQty'].append(tds[4].get_text())
                stock_summary['OrderBook']['SellSidePrice'].append(tds[3].get_text())
    
                 
                 
            print(json.dumps(stock_summary))
         
        browser.createAction(CommSec.REFRESH).click()
        end = time.time()
        print("Elapsed time for one extraction cycle=" + str(end - start) + "s")

total_securities = len(securities)
req_thread_count = 0
if (total_securities % securities_per_thread ) == 0:
    req_thread_count = total_securities // securities_per_thread
else:
    req_thread_count = total_securities // securities_per_thread + 1
print(str(req_thread_count) + " threads will be used for feed extraction")

threads = []

for i in range(0, req_thread_count):
    print("Starting thread " + str(i))
    print(securities[i*securities_per_thread:(i+1)*securities_per_thread])
    

    x = threading.Thread(target=extract_security_data, args=(securities[i*securities_per_thread:(i+1)*securities_per_thread] , i ))
    x.start()
    threads.append(x)
    
livecount = len(threads)    
while True:
    for t in threads:
        if t.is_alive():
            t.join(5)
        else:
            livecount -= 1
    if livecount <= 0:
        break
