import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
import setuptools.dist
import certifi
import time
import random
import schedule

from main import cookie_upgrades, affordable_upgrades

options = uc.ChromeOptions()
options.add_argument("--disable-popup-blocking")

driver = uc.Chrome(options=options, enable_cdp_events=True, incognito=True)

stealth(
    driver,
    vendor="Google Inc.",
    platform="MacIntel",
    webgl_vendor="Apple Inc.",
    renderer="Apple M1",
    fix_hairline=True,
)

options.add_argument("--remote-debugging-port=9222")

driver.get("https://orteil.dashnet.org/experiments/cookie/")
driver.implicitly_wait(1)

driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")


# Get cookie to click on.
cookie = driver.find_element(by=By.ID, value="cookie")

# Get upgrade item ids.
items = driver.find_elements(by=By.CSS_SELECTOR, value="#store div")
item_ids = [item.get_attribute("id") for item in items]

timeout = time.time() + 5
five_min = time.time() + 60 * 5

while True:
    cookie.click()

    if time.time() > timeout:
        all_prices = driver.find_elements(by=By.CSS_SELECTOR, value="#store b")
        item_prices = []

        for price in all_prices:
            element_text = price.text
            if element_text != "":
                cost = int(element_text.split("-")[1].strip().replace(",", ""))
                item_prices.append(cost)

        cookie_upgrades = {}
        for n in range(len(item_prices)):
            cookie_upgrades[item_prices[n]] = item_ids[n]

        ## Cookie count:
        money_element = driver.find_element(by=By.ID, value="money").text
        if "," in money_element:
            money_element = money_element.replace(",", "")
        cookie_count = int(money_element)

        ## Find upgrade items that it currently affords:
        affordable_upgrades = {}
        for cost, id in cookie_upgrades.items():
            if cookie_count >= cost:
                affordable_upgrades[cost] = id

        ## Purchase the most expensive affordable item:
        highest_price_labeled_item = max(affordable_upgrades)
        to_purchase_id = affordable_upgrades[highest_price_labeled_item]

        driver.find_element(By.ID, to_purchase_id).click()

        timeout = time.time() + 5

        # Stop the bots(cookie-clicking and item-checking bots) after 5 minutes:
        if time.time() > five_min:
            cookie_per_s = driver.find_element(by=By.ID, value="cps").text
            print(cookie_per_s)
            break






















