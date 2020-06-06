from azure.iot.device import IoTHubDeviceClient, Message

from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException

from datetime import datetime
import time

import json

CONNECTION_STRING = "HostName=sl-project.azure-devices.net;DeviceId=test;SharedAccessKey=AkvO6Oh3Kww1kxz3VOJdQip6rrtvpzvqa8Q5YRCF2UU="
MSG_TXT = dict()

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def iothub_run():

    try:
        client = iothub_client_init()
        print ( "IoT Hub device running" )

        while True:
            # Send the message.
            print("Getting data...")
            get_total()
            get_aus()
            final_msg = json.dumps(MSG_TXT)
            print("Sending message.")
            client.send_message(final_msg)
            now = datetime.now()
            curr_time = now.strftime("%Y-%m-%d %H:%M:%S")
            #print("Time sent: ", time)
            print ("Message successfully sent at {}, sending update in 20 seconds".format(curr_time))
            time.sleep(20)

    except KeyboardInterrupt:
        print ( "Client stopped" )

def get_total():
    # Installed chromedriver in the path chrome/chromedriver
    browser = webdriver.Chrome(executable_path="chrome/chromedriver")
    browser.get("https://www.worldometers.info/coronavirus")

    # Wait 10 seconds for page to load
    timeout = 10

    # Wait for the daily deaths chart to load, since it is the last thing to load in this website
    try:
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='main_table_countries_today']/tbody[3]/tr")))
    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()

    new = browser.find_element_by_xpath("//tr[@class='total_row']")
    data= new.text.split(" ")

    print(data)

    MSG_TXT['total_cases'] = data[1]
    MSG_TXT['new_cases_today'] = data[2]
    MSG_TXT['total_deaths'] = data[3]
    MSG_TXT['new_deaths_today'] = data[4]
    MSG_TXT['total_recovered'] = data[5]
    MSG_TXT['active_cases'] = data[6]

    news = browser.find_elements_by_xpath("//li[@class= 'news_li']")
    news_data = [x.text for x in news[:5]]
    clean_news = [x.replace('[source]','') for x in news_data]
    MSG_TXT['news'] = clean_news

    print(clean_news)

    browser.close()

def get_aus():
    # Installed chromedriver in the path chrome/chromedriver
    browser = webdriver.Chrome(executable_path="chrome/chromedriver")
    browser.get("https://covidlive.com.au/")

    # Wait 10 seconds for page to load
    timeout = 10

    # Wait for the daily deaths chart to load, since it is the last thing to load in this website
    try:
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.container")))
    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()

    au_cases = browser.find_element_by_xpath("//*[@id='content']/div/div[1]/section/table/tbody/tr[10]/td[2]").text
    nsw_cases = browser.find_element_by_xpath("//*[@id='content']/div/div[1]/section/table/tbody/tr[2]/td[2]").text
    nsw_active = browser.find_element_by_xpath("//*[@id='content']/div/div[2]/section/table/tbody/tr[2]/td[2]").text

    MSG_TXT['au_cases'] = au_cases
    MSG_TXT['nsw_cases'] = nsw_cases
    MSG_TXT['nsw_active'] = nsw_active

    browser.close()     


if __name__ == '__main__':
    #print ( "Getting data...\n" )
    #get_total()
    #get_aus()
    #final_msg = json.dumps(MSG_TXT)
    print ( "IoT Hub " )
    iothub_run()
    #now = datetime.now()
    #time = now.strftime("%Y-%m-%d %H:%M:%S")
    #print("Time sent: ", time)
    #print(final_msg)