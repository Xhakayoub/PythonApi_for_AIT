from requests_html import HTMLSession
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from selenium.webdriver.chrome.options import Options
from flask import Flask
from pyvirtualdisplay import Display


app = Flask(__name__)



@app.route('/<string:league>')
def get_data_by_league(league):
    chrome_options = Options()
    chrome_options.headless = True
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    browser = webdriver.Chrome('C:\\Users\\mouis\\webDriver\\chromedriver', options=chrome_options)
    browser.set_window_position(-10000,0)
    browser.get('https://fbref.com/en/comps/9/stats/Premier-League-Stats')
    elem = browser.find_element(
    By.XPATH, '//*[@id="all_stats_standard"]/div[1]/div/ul/li[1]')
    elem.click()
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="all_stats_standard"]/div[1]/div/ul/li[1]/div/ul/li[4]/button'))).click()
    csv = browser.find_element(By.XPATH, '//*[@id="csv_stats_standard"]')
    response = csv.text
    browser.close()
    browser.quit()
    return response

app.run(port=5000)
