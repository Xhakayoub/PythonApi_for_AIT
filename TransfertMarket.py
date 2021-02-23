from requests_html import HTMLSession
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from flask import Flask
from pyvirtualdisplay import Display
from selenium.common.exceptions import TimeoutException
import testConnection
import time
from unidecode import unidecode



app = Flask(__name__)


@app.route('/TransfertMarekt/<string:player>/<int:age>/<string:club>')
def get_player_data(player, age, club):

    data = {}

    chrome_options = Options()
    #chrome_options.headless = True
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("enable-automation")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.page_load_strategy = 'none'
    # chrome_options.add_argument("--disable-browser-side-navigation")
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    browser = webdriver.Chrome(
        'C:\\wamp64\\www\\chromedriver', options=chrome_options)
    # browser.set_page_load_timeout(5)
    browser.set_window_size(3840, 2160)

    link = 'https://www.transfermarkt.fr/'
    print(link)
    browser.get(link)

# Scapping the players's datas
    print(testConnection.test_connection())
    while testConnection.test_connection() == False:
        print('Waiting for internet ....')
        time.sleep(5)
    try:
        browser.maximize_window()
        inputElement = browser.find_element(
            By.XPATH, '//*[@id="schnellsuche"]/input[1]')
        inputElement.send_keys(player)
    
        inputElement.submit() 
    finally:
        header = browser.find_element_by_xpath('//*[@id="yw0"]/table/tbody')
        rows = header.find_elements_by_xpath('//*[@id="yw0"]/table/tbody/tr')
        print(len(rows))
        ifIsHim = False
        for x in range(len(rows)):
            response = {}
            #retrieve the name
            try:
                element = WebDriverWait(browser, 10, poll_frequency=2).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="yw0"]/table/tbody/tr['+str(x+1)+']/td[1]/table/tbody/tr[1]/td[2]/a')))
            finally:
                print(x+1)
                value = browser.find_element(
                    By.XPATH, '//*[@id="yw0"]/table/tbody/tr['+str(x+1)+']/td[1]/table/tbody/tr[1]/td[2]/a')
                print('________________________________________________')
                print(value.text)

                if(unidecode(value.text) == unidecode(player)): ifIsHim = True  
                else : ifIsHim = False

            #retrieve the club
            try:
                element = WebDriverWait(browser, 10, poll_frequency=2).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="yw0"]/table/tbody/tr['+str(x+1)+']/td[1]/table/tbody/tr[2]/td/a')))
            finally:
                value = browser.find_element(
                    By.XPATH, '//*[@id="yw0"]/table/tbody/tr['+str(x+1)+']/td[1]/table/tbody/tr[2]/td/a')
                print('________________________________________________')
                print(value.text)

                if(unidecode(value.text) == unidecode(club)): ifIsHim = True  
                else : ifIsHim = False

            #retrieve the age //*[@id="yw0"]/table/tbody/tr[1]/td[4]
            try:
                element = WebDriverWait(browser, 10, poll_frequency=2).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="yw0"]/table/tbody/tr['+str(x+1)+']/td[4]')))
            finally:
                value = browser.find_element(
                    By.XPATH, '//*[@id="yw0"]/table/tbody/tr['+str(x+1)+']/td[4]')
                print('________________________________________________')
                print(value.text)

                if(value.text == str(age)): ifIsHim = True  
                else : ifIsHim = False

            if(ifIsHim):  
                try:
                    element = WebDriverWait(browser, 10, poll_frequency=2).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="yw0"]/table/tbody/tr['+str(x+1)+']/td[6]')))
                finally:
                    value = browser.find_element(
                        By.XPATH, '//*[@id="yw0"]/table/tbody/tr['+str(x+1)+']/td[6]')
                    print('________________________________________________')
                    print(value.text)
                
                response = value.text    
                data["value"] = response
                break
    return data

    browser.close()
    browser.quit()


@app.route('/all/TransfertMarekt')
def get_all_data():

    data = {}

    chrome_options = Options()
    #chrome_options.headless = True
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("enable-automation")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.page_load_strategy = 'none'
    # chrome_options.add_argument("--disable-browser-side-navigation")
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    browser = webdriver.Chrome(
        'C:\\wamp64\\www\\chromedriver', options=chrome_options)
    # browser.set_page_load_timeout(5)
    browser.set_window_size(3840, 2160)

    link = 'https://www.transfermarkt.fr/spieler-statistik/wertvollstespieler/marktwertetop'
    print(link)
    browser.get(link)

# Scapping the players's datas
    print(testConnection.test_connection())
    while testConnection.test_connection() == False:
        print('Waiting for internet ....')
        time.sleep(5)

    browser.maximize_window()
    element = browser.find_element(
        By.XPATH, '/html/body/div/div[3]/div[3]/div[2]/button')
    element.click()

    header = browser.find_element_by_xpath('//*[@id="yw1"]/table/tbody')
    rows = header.find_elements_by_xpath('//*[@id="yw1"]/table/tbody/tr')
    print(len(rows))
    for y in range(19):
        for x in range(len(rows)):
            response = {}
            try:
                element = WebDriverWait(browser, 10, poll_frequency=2).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id = "yw1"]/table/tbody/tr['+str(x+1)+']/td[2]/table/tbody/tr[1]/td[2]/a')))
            finally:
                print(x+1)
                value = browser.find_element(
                    By.XPATH, '//*[@id = "yw1"]/table/tbody/tr['+str(x+1)+']/td[2]/table/tbody/tr[1]/td[2]/a')
                print('________________________________________________')
                print(value.text)
                response['name'] = value.text
            try:
                element = WebDriverWait(browser, 10, poll_frequency=2).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="yw1"]/table/tbody/tr['+str(x+1)+']/td[6]/b')))
            finally:
                value = browser.find_element(
                    By.XPATH, '//*[@id="yw1"]/table/tbody/tr['+str(x+1)+']/td[6]/b')
                print('________________________________________________')
                print(value.text)
                response['value'] = value.text
            data[x] = response
        try:
            element = WebDriverWait(browser, 10, poll_frequency=2).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="yw2"]/li[13]/a')))
        finally:
            browser.execute_script("arguments[0].scrollIntoView();", element)
            element = browser.find_element(
                By.XPATH, '//*[@id="yw2"]/li[13]/a')
            element.click()

    return data

    browser.close()
    browser.quit()


app.run(port=5000)
