import time
import random

from BrowserWindow import BrowserWindow
from CommSecDefs import CommSec
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from CommonDefs import Fields
from Password import *

class Producer:
    def __init__(self, consumer_group, syncgroup):
        self.consumer_group = consumer_group
        self.security_group = syncgroup
        self.browser = BrowserWindow()#headless=False)
    
    def getOBSideSummary(self,str):
        astr = str.split('for')
        return astr[0].split()[0].strip().replace(',',''), astr[1].split()[0].strip().replace(',','')
    
    def extract(self, consumer):
        self.browser.createAction(CommSec.REFRESH).click()
        stock_summary = {}
        stock_summary[Fields.NAME] = ((self.browser.createAction(CommSec.INSTRUMENT_DETAILS).get_text().split('<'))[0]).strip()
        stock_summary[Fields.EXCHANGE_CODE] = self.browser.createAction(CommSec.EXCHANGE_CODE).get_text()
        stock_summary[Fields.SECURITY_CODE] = self.browser.createAction(CommSec.SECURITY_CODE).get_text()
        stock_summary[Fields.LAST_PRICE] = ((self.browser.createAction(CommSec.LAST_PRICE).get_text().split('<'))[0]).strip()
        stock_summary[Fields.TODAYS_CHANGE] = self.browser.createAction(CommSec.TODAYS_CHANGE_AMOUNT).get_text(1).strip()

        items = self.browser.createAction(CommSec.STOCK_DETAILS_ITEM)._find_all()
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
                 
        items = self.browser.createAction(CommSec.STOCK_DETAILS_ITEM_SINGLE_FIELD)._find_all()
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
         
        stock_summary[Fields.ORDERBOOK] = {}
        stock_summary[Fields.ORDERBOOK]['BuySideNumber'] = []
        stock_summary[Fields.ORDERBOOK]['BuySideQty'] = []
        stock_summary[Fields.ORDERBOOK]['BuySidePrice'] = [] 
        stock_summary[Fields.ORDERBOOK]['SellSideNumber'] = []
        stock_summary[Fields.ORDERBOOK]['SellSideQty'] = []
        stock_summary[Fields.ORDERBOOK]['SellSidePrice'] = [] 
         
        items = self.browser.createAction(CommSec.ORDER_BOOK)._find_all()
        for i in range(0, len(items)):
            ih = items[i].get_attribute('innerHTML')
            soup = BeautifulSoup(ih, 'html.parser')
            tds = soup.find_all('td')
            stock_summary[Fields.ORDERBOOK]['BuySideNumber'].append(tds[0].get_text())
            stock_summary[Fields.ORDERBOOK]['BuySideQty'].append(tds[1].get_text())
            stock_summary[Fields.ORDERBOOK]['BuySidePrice'].append(tds[2].get_text())
            stock_summary[Fields.ORDERBOOK]['SellSideNumber'].append(tds[5].get_text())
            stock_summary[Fields.ORDERBOOK]['SellSideQty'].append(tds[4].get_text())
            stock_summary[Fields.ORDERBOOK]['SellSidePrice'].append(tds[3].get_text())
        
        
        stock_summary[Fields.BUYERS_COUNT], stock_summary[Fields.BUYERS_UNITS] = self.getOBSideSummary(self.browser.createAction(CommSec.MD_SUMMARY_BUYERS).get_text())
        stock_summary[Fields.SELLERS_COUNT], stock_summary[Fields.SELLERS_UNITS] = self.getOBSideSummary(self.browser.createAction(CommSec.MD_SUMMARY_SELLERS).get_text())
        
        
        return stock_summary
    
    def run(self, dummy):
        
        self.browser.openURL(CommSec.HOME_URL)
        self.browser.createAction(CommSec.CLIENT_ID).send_keys(COMMSEC_USERNAME).send_keys(Keys.TAB)
        self.browser.createAction(CommSec.PASSWORD).send_keys(COMMSEC_PASSWORD).send_keys(Keys.RETURN)
        print(self.browser.createAction(CommSec.ACCOUNT_DETAILS).get_text())
        
        for consumer in self.consumer_group:      
            self.browser.openTab(CommSec.SECURITY_PARTIAL_URL.replace('___', consumer.seccode))
        

        while True:
            if self.security_group.flag.get() == 1:
                print("Producer paused. Set flag to 0 to resume")
                time.sleep(1)
                continue
            
            wh = 0
            
            for consumer in self.consumer_group:
                wh = wh + 1
                self.browser.switchToTab(wh)
                
                
                product = self.extract(consumer)

                with consumer.cv:
                    consumer.data.append(product)
                    consumer.cv.notifyAll()
            
