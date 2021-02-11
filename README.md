# asxbots
Setup
   - Clone this repository; git clone https://github.com/doonyx/asxbots.git
   - Install eclipse for Java 
   - Install eclipse python extension PyDev. 
         - Open eclipse 
         - Go to help -> Install new software 
         - Add this link to lookup software sources http://www.pydev.org/updates
         - Select PyDev 
         - Install 
   - Restart eclipse 
   - Create a new PyDev project and change the default directory to your repository location which you just cloned. Please note you need to go inside of asxbots folder for this purpose
   - Create a new file called Password.py
   - Add 
      COMMSEC_USERNAME = '<your CommSec client ID>'
      COMMSEC_PASSWORD = '<your password>'
  - Do not stage (add to git) this file to the repository. You may include this in .gitingore if you may forget
  - Open main.py file and run it using eclipse 
  - You should be able to see extracted feed is dumping into your eclipse console 
