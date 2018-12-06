import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


# logs in, manages the game and closes the browser
def executeGameSession(player):
    # setup web browser
    browser = webdriver.Chrome('C:\\Users\\Nick\\AppData\\Local\\Programs\\chromeDriver\\chromedriver.exe')
    loginAndSelectWorld(browser, player)
    manageSenate(browser)
    reapVillages(browser)

    browser.quit()


# go to all available villages and reaps resources
def reapVillages(browser):
    #go to island view
    goToIslandViewButton = browser.find_element_by_class_name('island_view')
    goToIslandViewButton.click()
    time.sleep(1)
    browser.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)
    time.sleep(1)

    numVillagesReaped = 0
    # reap all villages that are available
    while len(browser.find_elements_by_class_name('claim')) > 0:
        # open village window
        villageLink = browser.find_elements_by_class_name('owned')[numVillagesReaped]
        villageLink.click()
        time.sleep(2)

        disabledBanners = browser.find_elements_by_class_name('actions_locked_banner')
        if len(disabledBanners) > 0:
            # click on button to collect resources
            collectResourcesButtons = browser.find_elements_by_class_name('card_click_area')
            collectResourcesButtons[1].click()
            time.sleep(1)

            # close village window
            browser.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)
            time.sleep(1)
            numVillagesReaped += 1


# logs the user in and navigates to the game world
def loginAndSelectWorld(browser, player):
    browser.get('https://us.grepolis.com/')
    time.sleep(2)

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
    time.sleep(2)

    #select world
    index = player['worldIndex']
    worldButton = browser.find_elements_by_class_name('world_name')[index]
    worldButton.find_element_by_css_selector('div').click()
    time.sleep(2)
    # exit any pop ups
    browser.find_element_by_tag_name('body').send_keys(Keys.ESCAPE) 
    time.sleep(1)
    browser.find_element_by_tag_name('body').send_keys(Keys.ESCAPE)

def manageSenate(browser):
    # go to the city overview
    browser.find_element_by_class_name('city_overview').click()
    time.sleep(1)
    
    warCoinBox = browser.find_element_by_class_name('war_coins_box')
    actions = ActionChains(browser)
    actions.move_to_element(warCoinBox).move_by_offset(-440, 0).click().perform()
    time.sleep(0.4)
