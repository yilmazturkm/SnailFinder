#
# Author: yilmazturkm
# Author Github: https://github.com/yilmazturkm
# Author Url: https://yilmazturk.gen.tr

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json
import requests

filterFile = open("settings.json")
variables = json.load(filterFile)

familyFilter = variables["Family"]
classFilter = variables["Class"]
generationFilter = variables["Generation"]
adaptationFilter = variables["Adaptation"]
purityFilter = variables["Purity"]
genderFilter = variables["Gender"]
priceFilter = variables["Price"]
telegramBotToken = variables["Telegram Bot Token"]
telegramChatId = variables["Telegram Chat ID"]

marketplaceUrl = "https://www.snailtrail.art/marketplace/snails"

chromeOptions = webdriver.ChromeOptions()
chromeOptions.add_argument("window-size=1800,1000")
chromeOptions.add_argument("no-sandbox")
chromeOptions.add_argument("disable-dev-shm-usage")
chromeOptions.add_argument("disable-gpu")
chromeOptions.add_argument("log-level=3")
#chromeOptions.add_argument("window-position=0,-1000")

def sendMessage(message):
    try:
        message = message.replace("#", "")
        botToken = telegramBotToken
        botChatID = telegramChatId
        textMessage = 'https://api.telegram.org/bot' + botToken + '/sendMessage?chat_id=' + botChatID + '&parse_mode=HTML&text=' + message
        response = requests.get(textMessage)
        return response
    except Exception as e:
        print(f"Error: {type(e)}")

def openFilterArea(browser):
    while True:
        try:
            browser.find_element(By.CLASS_NAME, "filter-button").click()
            break
        except Exception as e:
            pass


# Racing Filters
def selectFilter(browser, selection, filterClass):
    while True:
        try:
            browser.find_element(By.CLASS_NAME, filterClass).click()
            break
        except Exception as e:
            pass
    while True:
        try:
            classSelect = browser.find_elements(By.TAG_NAME, "p-dropdownitem")
            for i in classSelect:
                if (i.text).lower() in selection.lower():
                    i.click()
            break
        except Exception as e:
            pass

def multipleSelectFilter(browser, selection, filterClass):
    while True:
        try:
            browser.find_element(By.CLASS_NAME, filterClass).click()
            break
        except Exception as e:
            pass
    while True:
        try:
            classSelect = browser.find_elements(By.CLASS_NAME, "p-ripple.p-element.p-multiselect-item")
            for i in classSelect:
                if i.text in selection:
                    i.click()
            break
        except Exception as e:
            pass
def applySelection(browser):
    while True:
        try:
            buttons = browser.find_element(By.CLASS_NAME, "filter-item-btn")
            applyButton = buttons.find_elements(By.TAG_NAME, "button")
            applyButton[1].click()
            time.sleep(2)
            break
        except Exception as e:
            pass

def getSnailList(browser):
    html = browser.find_element(By.TAG_NAME, 'html')
    html.send_keys(Keys.HOME)
    noSnailItem = browser.find_elements(By.CLASS_NAME, "mt-4.fw-bold")
    if len(noSnailItem) > 0:
        return False
    snailNameList = list()
    snailLinkList = list()
    snailList = list()
    while True:
        time.sleep(3)
        snailsListItems = browser.find_elements(By.TAG_NAME, "sts-snail")
        html.send_keys(Keys.PAGE_DOWN)
        for i in snailsListItems:
            snailName = i.find_element(By.CLASS_NAME, "snail__title").text
            if snailName not in snailNameList:
                snailLinkItem = i.find_element(By.TAG_NAME, "a")
                snailLink = snailLinkItem.get_attribute("href")
                snailLinkList.append(snailLink)
                snailPrice = i.find_element(By.CLASS_NAME, "snail__price").text
                snailNameList.append(snailName)
                if float(snailPrice) > priceFilter:
                    return snailList
                snailList.append([snailName, snailPrice])

allSnailsDict = dict()
def getSnailDetails(browser, snailLink):
    global allSnailsDict
    browser.get(snailLink)
    time.sleep(1)
    htmlItem = browser.find_element(By.TAG_NAME, "html")
    while True:
        try:
            htmlItem.send_keys(Keys.PAGE_DOWN)
            snailName = browser.find_element(By.CLASS_NAME, "snail-name.public.ng-star-inserted").text
            snailInfoBoxItems = browser.find_elements(By.TAG_NAME, "sts-snail-info-box")
            snailPriceItem = browser.find_element(By.CLASS_NAME, "btn.btn-primary.ng-star-inserted").text
            break
        except Exception as e:
            time.sleep(1)
            pass
    snailPrice = snailPriceItem.split()[-1]
    snailItemsDict = dict()
    snailItemsDict["Price"] = snailPrice
    for i in snailInfoBoxItems:
        itemText = i.find_element(By.CLASS_NAME, "p-element.snail-info-box.ng-star-inserted").text
        itemText = itemText.split("\n")
        if len(itemText) > 1:
            snailItemsDict[itemText[0]] = itemText[1]
    allSnailsDict[snailName] = snailItemsDict
    return True
browser = webdriver.Chrome(options=chromeOptions)
while True:
    browser.get(marketplaceUrl)

    openFilterArea(browser)
    if len(familyFilter) > 0:
        filterClass = "p-dropdown-trigger-icon.ng-tns-c74-3.pi.pi-chevron-down"
        selectFilter(browser, familyFilter, filterClass)
    if len(classFilter) > 0:
        filterClass = "p-dropdown-trigger-icon.ng-tns-c74-4.pi.pi-chevron-down"
        selectFilter(browser, classFilter, filterClass)
    if len(generationFilter) > 0:
        filterClass = "p-dropdown-trigger-icon.ng-tns-c74-5.pi.pi-chevron-down"
        selectFilter(browser, generationFilter, filterClass)
    if len(adaptationFilter) > 0:
        filterClass = "p-multiselect-trigger-icon.ng-tns-c76-6.pi.pi-chevron-down"
        multipleSelectFilter(browser, adaptationFilter, filterClass)
    if len(purityFilter) > 0:
        filterClass = "p-dropdown-trigger-icon.ng-tns-c74-7.pi.pi-chevron-down"
        selectFilter(browser, purityFilter, filterClass)
    if len(genderFilter) > 0:
        filterClass = "p-dropdown-trigger-icon.ng-tns-c74-8.pi.pi-chevron-down"
        selectFilter(browser, genderFilter, filterClass)
    applySelection(browser)

    snailList = getSnailList(browser=browser)
    if snailList == False:
        print(f"No snails exists")
    else:
        message = f"{len(snailList)} Snails Found\n"
        for i in snailList:
            message += f"[Snail Name: {i[0]}] [Price: {i[1]} AVAX]\n"
        print(message)


