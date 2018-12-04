import time
import json
from webDriver import executeGameSession

file = open('settings.json', 'r')
settings = json.loads(file.read())
file.close()

executeGameSession(settings['player'])