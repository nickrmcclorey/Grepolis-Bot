import time
import json
import random
from datetime import datetime  
from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from Building import Building

def play_grepolis(flag, update_function, finish_function):
    update_function('Loading Settings')
    file = open('settings.json', 'r')
    settings = json.loads(file.read())
    file.close()
  
    endTime = datetime.now() + timedelta(hours = settings['player']['max_hours_to_run'])
    remaining_cycles = settings['player']['max_sessions'] or 9999

    print('don\'t end the program while the web browser is open')
    while datetime.now() < endTime and remaining_cycles > 0 and flag.get() == False:

        executeGameSession(settings, update_function)

        remaining_cycles -= 1
        secondsToWait = parse_seconds(settings['player']['frequency'])
        next_session = datetime.now() + timedelta(seconds=secondsToWait)
        if next_session > endTime or remaining_cycles <= 0 or flag.get():
            break

        update_function('succesfully played game session, next login scheduled for ' + str(next_session.hour) + ':' + str(next_session.minute))
        wait(secondsToWait, flag)

    update_function('finished playing')
    finish_function()


def wait(seconds, flag):
    return_time = datetime.now() + timedelta(seconds=seconds)
    while datetime.now() < return_time and flag.get() == False:
        time.sleep(1)


# logs in, manages the game and closes the browser
def executeGameSession(settings, update_function):
    # setup web browser
    exePath = settings['webDriver']["executablePath"]
    browser = None
    if (settings["webDriver"]["browser"] == 'firefox'):
        browser = webdriver.Firefox(executable_path=exePath)
    else:
        browser = webdriver.Chrome(exePath)
    browser.maximize_window()


    try:
        update_function('Navigating to Grepolis webiste')
        loginAndSelectWorld(browser, settings['player'])
        firstCity = browser.find_element_by_class_name('town_name').text
        currentCity = None

        # cycle through all the cities and farm resources or build buildings
        while currentCity != firstCity:
            currentCity = browser.find_element_by_class_name('town_name').text
            if (settings['player']['reapVillages']):
                update_function('Farming resources from villages for ' + currentCity)
                reapVillages(browser)
            if (settings['player']['manageSenate']):
                update_function('Upgrading buildings in ' + currentCity)
                upgradgeBuildings(browser, settings['buildings'])
            click(browser.find_element_by_class_name('btn_next_town'))
    except Exception as e:
        print(e)
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
    time.sleep(5)

    #select world
    worldButton = browser.find_elements_by_class_name('world_name')
    worldButton[0].find_element_by_css_selector('div').click()
    time.sleep(2)

    # exit any pop ups
    pressEscape(browser)
    time.sleep(1)
    pressEscape(browser)


def upgradgeBuildings(browser, buildingSettings):
    click(browser.find_element_by_class_name('city_overview'))
    click(browser.find_element_by_id('building_main_area_main'))
    manageSenate(browser, buildingSettings)


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

def manageSenate(browser, buildingSettings):
    
    buildings = buildingArray(browser, buildingSettings)
    if (len(buildings) > 0):
        # upgradge building whose furthest from goal
        buildingToUpgrade = min(buildings, key = lambda x: x.percentToGoal())
        buildingToUpgrade.htmlButton.click()
    
    time.sleep(1)
    pressEscape(browser)
    time.sleep(0.4)
    pressEscape(browser)
    time.sleep(1)


def buildingArray(browser, buildingSettings):
    
    allButtons = browser.find_elements_by_class_name('build_up')
    buildings = []

    k = 0
    while k < len(buildingSettings):
        newBuilding = Building(buildingSettings[k], allButtons[k])
        if newBuilding.haveEnoughResources:
            buildings.append(newBuilding)
        k += 1

    return buildings