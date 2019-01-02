import sys
import time
import json
import random
from datetime import datetime  
from datetime import timedelta
from webDriver import executeGameSession

hoursToRun = 0
if len(sys.argv) > 1:
    hoursToRun = float(sys.argv[1])
else:
    hoursToRun = float(input('How many hours do you want to run? \n'))
        
endTime = datetime.now() + timedelta(hours = hoursToRun)

print('don\'t end the program while the web browser is open')
while (datetime.now() < endTime):
    file = open('settings.json', 'r')
    settings = json.loads(file.read())
    file.close()

    executeGameSession(settings)
    secondsToWait = random.randint(60 * 20, 60 * 25)

    if datetime.now() + timedelta(seconds=secondsToWait) > endTime:
        break

    print('succesfully played login session, next login in', secondsToWait / 60, ' minutes')
    time.sleep(secondsToWait)

print('finished playing')