import time
import json
import random
from datetime import datetime  
from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from Building import Building

def play_grepolis():
    file = open('settings.json', 'r')
    settings = json.loads(file.read())
    file.close()
            
    endTime = datetime.now() + timedelta(hours = settings['player']['max_hours_to_run'])

    print('don\'t end the program while the web browser is open')
    while (datetime.now() < endTime):

        executeGameSession(settings)
        secondsToWait = parse_seconds(settings['player']['frequency'])

        if datetime.now() + timedelta(seconds=secondsToWait) > endTime:
            break

        print('succesfully played login session, next login in', secondsToWait / 60, ' minutes')
        time.sleep(secondsToWait)

    print('finished playing')


# logs in, manages the game and closes the browser
def executeGameSession(settings):
    # setup web browser
    exePath = settings['webDriver']["executablePath"]
    browser = None
    if (settings["webDriver"]["browser"] == 'firefox'):
        browser = webdriver.Firefox(executable_path=exePath)
    else:
        browser = webdriver.Chrome(exePath)
    browser.fullscreen_window()


    try:
        loginAndSelectWorld(browser, settings['player'])
        firstCity = browser.find_element_by_class_name('town_name').text
        currentCity = None

        # cycle through all the cities and farm resources or build buildings
        while currentCity != firstCity:
            if (settings['player']['reapVillages']):
                reapVillages(browser)
            if (settings['player']['manageSenate']):
                upgradgeBuildings(browser, settings['buildings'])
            click(browser.find_element_by_class_name('btn_next_town'))
            currentCity = browser.find_element_by_class_name('town_name').text
    except:
        browser.quit()
        print('something went wrong')

    browser.quit()


# go to all available villages and reaps resources
def reapVillages(browser):
    #go to island view
    goToIslandViewButton = browser.find_element_by_class_name('island_view')
    showCurrentIslandButton = browser.find_element_by_class_name('btn_jump_to_town')
    click(goToIslandViewButton)
    click(showCurrentIslandButton)
    pressEscape(browser)

    # reap all villages that are available
    while len(browser.find_elements_by_class_name('claim')) > 0:
        pressEscape(browser)
        # open village window
        villageLink = browser.find_element_by_class_name('claim')
        actions = ActionChains(browser)
        actions.move_to_element(villageLink).click().perform()
        time.sleep(1)

        # make sure we're allowed to collect resources
        if len(browser.find_element_by_class_name('pb_bpv_unlock_time').text) == 0:
            # click on button to collect resources
            collectResourcesButtons = browser.find_elements_by_class_name('card_click_area')
            click(collectResourcesButtons[0])
            pressEscape(browser)

        # close village window
        pressEscape(browser)


# logs the user in and navigates to the game world
def loginAndSelectWorld(browser, player):
    #browser.maximize_window()
    browser.get('https://us.grepolis.com/')
    time.sleep(1)

    # find username and password inputs
    usernameInput = browser.find_element_by_id('login_userid')
    passwordInput = browser.find_element_by_id('login_password')

    # enter user name and password
    usernameInput.send_keys(player['username'])
    time.sleep(1)
    passwordInput.send_keys(player['password'])
    time.sleep(1)

    #press login button
    loginButton = browser.find_element_by_id('login_Login')
    loginButton.click()
    time.sleep(10)

    #select world
    worldButton = browser.find_elements_by_class_name('world_name')
    worldButton[0].find_element_by_css_selector('div').click()
    time.sleep(2)

    # exit any pop ups
    pressEscape(browser)
    time.sleep(1)
    pressEscape(browser)


def upgradgeBuildings(browser, buildingSettings):
    browser.find_element_by_class_name('city_overview').click()
    time.sleep(1)
    browser.find_element_by_class_name('js-tutorial-btn-construction-mode').click()
    time.sleep(1)
    panels = browser.find_elements_by_class_name('city_overview_overlay')
    panels.pop(2)
    buildings = []

    for k in range(0, 12):
        if len(panels[k].find_elements_by_class_name('disabled')) == 0:
            buildings.append(Building(buildingSettings[k], panels[k]))

    if (len(buildings) > 0):
        # upgradge building whose furthest from goal
        buildingToUpgrade = min(buildings, key = lambda x: x.percentToGoal())
        buildingToUpgrade.htmlButton.click()
        time.sleep(1)


def parse_seconds(string):
    minutes = 'hours' not in string
    number_minutes = int(string.strip('minutes').strip('hours').strip(' '))
    if minutes == False:
        number_minutes *= 60

    return random.randint(60 * number_minutes, 60 * (number_minutes + 5))

def pressEscape(browser):
    browser.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)
    time.sleep(1)


def click(webElement):
    webElement.click()
    time.sleep(1)