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
from SyncGroup import SyncGroup


# securities = ['ATH', 'XST', 'SCU', 'FRX', 'CCE', 'CAV', 'IXR', 'IOU', 'CRL', 'PWN', 'CLZ', 'UUV', 'BSM', 'AZI', 'SYA'] 
# securities = [
#                 ['CGB', 'ACW', 'MXC', 'BRK'],
#                 ['EQE', 'AUZ', 'CPH', 'BSM'], 
#                 ['CCE', 'GGX', 'MSB', 'NWS'], 
#                 ['PLL', 'BPT', 'AMP'] 
# 
#              ]

securities = [
                ['PLS']

             ]
        
        
def rungroup(secgrp):             
    sg = SyncGroup(secgrp)
    sg.run()
    
threads = []
for secgrp in securities:
    t = threading.Thread(name='secgrp', target=rungroup, args=(secgrp,))
    threads.append(t)
    t.start()
    
while True:
    for t in threads:
        t.join(3)      
