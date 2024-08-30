from app import *
from web import *

import threading


threadWeb = threading.Thread(target=web.run).start()
app = App()
thread = threading.Thread(target=App.ini(App)).start()
      
    
exit()