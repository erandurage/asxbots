'''

Created on 9 Feb 2021



#kjkjk
@author: eran
'''

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

actionWaitSeconds = 600
    
class Action:
    def __init__(self, driver, xpath=''):
        self.driver = driver
        self.xpath = xpath
        
 
    def locate(self, element_xpath=''):
        p = element_xpath if element_xpath != '' else self.xpath
        return WebDriverWait(self.driver, actionWaitSeconds).until(
            EC.visibility_of_element_located((By.XPATH, p))
        )
    def _locate(self):
        return WebDriverWait(self.driver, actionWaitSeconds).until(
            EC.visibility_of_element_located((By.XPATH, self.xpath))
        )
        
    def _find(self):
        return WebDriverWait(self.driver, actionWaitSeconds).until(
            EC.presence_of_element_located((By.XPATH, self.xpath))
        )
        
    def _find_all(self):
        self._find()
        return self.driver.find_elements(By.XPATH, self.xpath )
    
    def get_all_values(self):
        self._find()
        ret = []
        for e in self.driver.find_elements(By.XPATH, self.xpath ):
            v = e.get_attribute('innerHTML')
            ret.append(v)
        return ret
        
    
    def _relocate(self, n):
        self._find()
        e = self.driver.find_elements(By.XPATH, self.xpath )
        return e[n]
    
    def _click(self):
        e = WebDriverWait(self.driver, actionWaitSeconds).until(
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
        actions_to_perform = ActionChains(self.driver)
        for k in keys_to_send:
            actions_to_perform.send_keys(k)
        actions_to_perform.perform()
    
    def get_value(self):
        """
        We need to optimise this method
        """
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
        return self._relocate(n).get_attribute('innerHTML')

    def get_HTML(self):
        s = self._find()
        return s.get_attribute('innerHTML')
    
    def print_all(self):
        es = self._find_all()
        for e in es:
            print(e.get_attribute('innerHTML'))
