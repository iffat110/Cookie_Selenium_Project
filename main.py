from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

TIMEOUT_DURATION = 60 * 5   
VERIFICATION = 5

service = Service(executable_path='C:\Development\chromedriver')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://orteil.dashnet.org/experiments/cookie/")

cookie = driver.find_element(By.ID, "cookie")

items = driver.find_elements(By.CSS_SELECTOR, "#store div")
item_ids = [item.get_attribute("id") for item in items[:-1]]  # eliminating the last element with no price
print(item_ids)

timeout = time.time() + TIMEOUT_DURATION
time_verification = time.time() + VERIFICATION


def buy_upgrade():

    # Get my current cookie balance
    money = driver.find_element(By.ID, "money").text
    money = int(money.replace(",", ""))

    # Get current upgrade prices (since they change with time)
    all_prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
    item_prices = []
    for price in all_prices:
        element_text = price.text
        if element_text != "":      # There is a empty element
            cost = int(element_text.split('-')[1].strip().replace(',', ''))
            item_prices.append(cost)
    print(item_prices)

    # Find and buy the most expensive element and break for-loop
    for index in range(1, len(item_prices) + 1):
        if money > item_prices[-index]:
            buy_element = driver.find_element(By.ID, item_ids[-index])
            buy_element.click()
            print(f"Cookies: {money}")
            print(f"Buying 1 {item_ids[-index][3:]}")
            break


while True:
    cookie.click()

    if time.time() > time_verification:
        time_verification = time.time() + VERIFICATION
        buy_upgrade()

    if time.time() > timeout:
        cps = driver.find_element(By.ID, "cps")
        print(f"Cookies/second: {cps.text}")
        break

input("press any key to stop....")
driver.quit()


driver.close()

