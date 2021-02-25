from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from Action import Action
import os 

#te
class BrowserWindow:
    def __init__(self, headless=True):
        options = Options()
        options.add_experimental_option("prefs", {
          "download.default_directory": r""+os.path.dirname(os.path.realpath(__file__)) +"",
          "download.prompt_for_download": False,
          "download.directory_upgrade": True,
          "safebrowsing.enabled": True
        })

        if headless:
            options.add_argument("--headless") 
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.driver.maximize_window()
    
    def openURL(self, url):
        self.driver.get(url)
        
    def openTab(self, url):
        self.driver.execute_script("window.open('"+url+"');")
        
    def switchToTab(self, tabid):
        self.driver.switch_to.window(self.driver.window_handles[tabid])
    
    def closeCurrentTab(self):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        
    def createAction(self, xpath=''):
        return Action(self.driver , xpath)
    
    def close(self):
        self.driver.delete_all_cookies()
        self.driver.close()
        print("Browser successfully closed!")
        
    def getTitle(self):
        return self.driver.title