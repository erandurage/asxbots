'''
Created on 3 Feb 2021

@author: Banner
'''
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import traceback
import inspect
import time
import random
import json
from bs4 import BeautifulSoup

options = Options()
# options.add_argument("--headless") 
config = {}
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
config['URL'] = 'https://www2.commsec.com.au/quotes/summary?stockCode=___&exchangeCode=ASX'
class _ActionStep:
    def __init__(self, xpath=''):
        self.driver = ElementFactory.instance().get_driver()
        self.xpath = xpath
        
 
    def locate(self, element_xpath=''):
        p = element_xpath if element_xpath != '' else self.xpath
        return WebDriverWait(driver, 600).until(
            EC.visibility_of_element_located((By.XPATH, p))
        )
    def _locate(self):
        return WebDriverWait(driver, 600).until(
            EC.visibility_of_element_located((By.XPATH, self.xpath))
        )
        
    def _find(self):
        return WebDriverWait(driver, 600).until(
            EC.presence_of_element_located((By.XPATH, self.xpath))
        )
        
    def _find_all(self):
        self._find()
        return self.driver.find_elements(By.XPATH, self.xpath )
    
    def _relocate(self, n):
#         print("relocate with " + str(n))
        self._find()
#         print('located')
        e = self.driver.find_elements(By.XPATH, self.xpath )
        return e[n]
    
    def _click(self):
        e = WebDriverWait(driver, 600).until(
            EC.visibility_of_element_located((By.XPATH, self.xpath))
        )
        e.click()
        return e
    def click(self):
        self._click()
        return self
    def send_keys(self, keys_to_send):
        e = self._click()
        e.send_keys(keys_to_send)
        return self
    
    def send_key_sequence(self, *keys_to_send):
        actions_to_perform = ActionChains(driver)
        for k in keys_to_send:
            actions_to_perform.send_keys(k)
        actions_to_perform.perform()
    
    def get_value(self):
        retries = 0
        attr = ''
        while True:
            e = self._locate()
            roprop = e.get_attribute('readonly')
            print(roprop)
            attr = e.get_attribute('title')
            if roprop or roprop == 'true':
                print("Readonly attribute is there")
                if attr == None:
                    attr = ''
                return attr
                
            if attr == None or attr =='':
                attr = e.get_attribute('value')
                print("Get value value="+attr+"|")
                if attr == None or attr =='':
                    if retries == 100:
                        raise ValueError("Value not found")
                    print("Trying again to get_value")
                    time.sleep(1)
                    retries += 1
                    continue
                
            break
        return attr

    def get_text(self, n=0):
#         print("Getting text of " + self.xpath)

        
#         print("With array")
        return self._relocate(n).get_attribute('innerHTML')
    
    def print_all(self):
        es = self._find_all()
        for e in es:
            print(e.get_attribute('innerHTML'))
        
class Singleton:
    """
    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.

    The decorated class can define one `__init__` function that
    takes only the `self` argument. Also, the decorated class cannot be
    inherited from. Other than that, there are no restrictions that apply
    to the decorated class.

    To get the singleton instance, use the `instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.

    """

    def __init__(self, decorated):
        self._decorated = decorated

    def instance(self):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.

        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)
@Singleton
class ElementFactory:
    def set_driver(self, driver):
        self.driver = driver
    
    def get_driver(self):
        return self.driver
    

def GenerateRandomName():
    name = ''
    for x in range(0,5):
        name += chr(random.randint(0,25)+65)
        
    for x in range(random.randrange(7)):
        name += chr(random.randint(0,25)+65)
        
    return name



def add_to_summary(stock_summary, key, xpath, n=0):
    stock_summary[key] = _ActionStep(xpath).get_text(n)
   
        
try:
    ElementFactory.instance().set_driver(driver)
    driver.maximize_window()
#     securities = ['ATH', 'XST', 'SCU', 'FRX', 'CCE', 'CAV', 'IXR', 'IOU', 'CRL', 'PWN', 'CLZ', 'UUV', 'BSM', 'AZI', 'SYA']
    securities = ['BHP', 'SVW', 'ATH']
    driver.get('https://www2.commsec.com.au/')
    _ActionStep('//input[@id="ctl00_cpContent_txtLogin"]').send_keys('56352429').send_keys(Keys.TAB)
    _ActionStep('//input[@id="ctl00_cpContent_txtPassword"]').send_keys('Subotaei1!CSEC').send_keys(Keys.RETURN)
    
    print(_ActionStep('//span[@id="ctl00_BodyPlaceHolder_HomePrivateView1_settlementWidget_ddAccountList_lblAccount_field"]').get_text())
    
    print("CommSec logged in...loading securities")
   
    securl = 'https://www2.commsec.com.au/quotes/summary?stockCode=___&exchangeCode=ASX'
    for seccode in securities:      
        driver.execute_script("window.open('"+config['URL'].replace('___', seccode)+"');")
    
    
    print(len(driver.window_handles))
    
    
    while True:
        start = time.time()
        for wh in range(1, len(driver.window_handles)):
            driver.switch_to.window(driver.window_handles[wh])
            stock_summary = {}
            stock_summary['Name'] = ((_ActionStep('//h1[@class="instrument-details__stock"]').get_text().split('<'))[0]).strip()
            stock_summary['Exchange Code'] = _ActionStep('//span[@id="overview-exchange-code"]').get_text()
            stock_summary['Security Code'] = _ActionStep('//span[@id="overview-security-code"]').get_text()
            stock_summary['Last price'] = ((_ActionStep('//span[@class="stock-price__last-price-value"]').get_text().split('<'))[0]).strip()
            stock_summary['Todays Change'] = _ActionStep('//span[@class="stock-price__todays-change-amount"]').get_text(1).strip()
           
            add_to_summary(stock_summary, 'Last Price', '//span[@class="stock-price__last-price-value"]')
            add_to_summary(stock_summary, 'Todays Change Amount', '//span[@class="stock-price__todays-change-amount"]', 1)
            
            items = _ActionStep('//li[@class="stock-details__item"]')._find_all()
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
                    
            items = _ActionStep('//li[@class="stock-details__item ng-star-inserted"]')._find_all()
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
            
            items = _ActionStep('//tr[@class="qr-table__row ng-star-inserted"]')._find_all()
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
        
        _ActionStep('//button[@class="button button--clean header-button"]').click()
        end = time.time()
        print("Elapsed time for one extraction cycle=" + str(end - start) + "s")

     
    

except:
    print("Generic exception")
    traceback.print_exc()
    var = traceback.format_exc()
    print(var)
finally:

    

    driver.delete_all_cookies()
    driver.close()
    print("Browser successfully closed!")


