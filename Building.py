class Building:
    
    def __init__(self, json, htmlButton):
        self.name = json['name']
        self.maxLevel = json['maxLevel']
        self.htmlButton = htmlButton
        buttonText = htmlButton.text
        if buttonText.lower() == 'not possible':
            self.haveEnoughResources = False
        else:
            self.haveEnoughResources = True
            self.level = int(htmlButton.text.replace('Expansion to ', '').replace('Build', '0'))

    def percentToGoal(self):
        return self.level / self.maxLevel
