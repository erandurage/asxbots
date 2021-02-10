from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from Action import Action

class BrowserWindow:
    def __init__(self):
        options = Options()
        options.add_argument("--headless") 
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.driver.maximize_window()
    
    def openURL(self, url):
        self.driver.get(url)
        
    def openTab(self, url):
        self.driver.execute_script("window.open('"+url+"');")
        
    def switchToTab(self, tabid):
        self.driver.switch_to.window(self.driver.window_handles[tabid])
        
    def createAction(self, xpath=''):
        return Action(self.driver , xpath)
    
    def close(self):
        self.driver.delete_all_cookies()
        self.driver.close()
        print("Browser successfully closed!")