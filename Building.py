class Building:
    
    def __init__(self, json, panel):
        self.name = json['name']
        self.maxLevel = json['maxLevel']
        self.htmlButton = panel.find_element_by_class_name('btn_build')
        self.level = int(panel.find_elements_by_css_selector('span')[2].text)

    def percentToGoal(self):
        return self.level / self.maxLevel
