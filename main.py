import time
import json
import random
import threading
from datetime import datetime  
from datetime import timedelta  
from webDriver import executeGameSession


endTime = datetime.now() + timedelta(hours = 8)
while (datetime.now() < endTime):
    file = open('settings.json', 'r')
    settings = json.loads(file.read())
    file.close()
    executeGameSession(settings)
    print('succesfully reaped resources')
    secondsToWait = random.randint(60 * 20, 60 * 25)
    time.sleep(secondsToWait)
