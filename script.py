from azure.iot.device import IoTHubDeviceClient, Message

from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException

from datetime import datetime

# Installed chromedriver in the path chrome/chromedriver
browser = webdriver.Chrome(executable_path="chrome/chromedriver")
browser.get("https://www.worldometers.info/coronavirus")

# Wait 10 seconds for page to load
timeout = 10

# Wait for the daily deaths chart to load, since it is the last thing to load in this website
try:
    WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.tabbable-panel-deaths")))
except TimeoutException:
    print("Timed out waiting for page to load")
    browser.quit()

new = browser.find_element_by_xpath("//tr[@class= 'total_row']")
row = new.find_element_by_xpath("./..")
data = row.text.split(" ")

world_total = []

total_cases = data[1]
new_cases_today = data[2]
total_deaths = data[3]
new_deaths_today = data[4]
total_recovered = data[5]
active_cases = data[6]

now = datetime.now()
time = now.strftime("%Y-%m-%d %H:%M:%S")

print("Current Time =", time)

