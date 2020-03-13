from requests_html import HTMLSession
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

session = HTMLSession()
browser = webdriver.Chrome('C:\\Users\\mouis\\webDriver\\chromedriver') 

browser.get('https://fbref.com/en/comps/9/stats/Premier-League-Stats')


elem = browser.find_element(By.XPATH, '//*[@id="all_stats_standard"]/div[1]/div/ul/li[1]')

elem.click()
#last_height = browser.execute_script("return document.body.scrollHeight")
#browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#elem1 = browser.find_element(By.XPATH, '//*[@id="all_stats_standard"]/div[1]/div/ul/li[1]/div/ul/li[4]/button')

WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="all_stats_standard"]/div[1]/div/ul/li[1]/div/ul/li[4]/button'))).click()
csv = browser.find_element(By.XPATH, '//*[@id="csv_stats_standard"]')

print(csv.text)

#ActionChains(browser).move_to_element(elem1).click().perform() # item.click()

