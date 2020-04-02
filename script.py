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

types = ['keepers', 'stats', 'passing', 'shooting', 'playingtime', 'keepersadv', 'misc']
competitions = [9, 12, 8, 13, 11, 19, 20] 

def get_league_by_number(argument): 
    switcher = { 
        13: "Ligue-1-Stats", 
        8: "Champions-League-Stats",     
        11: "Serie-A-Stats",
        19: "Europa-League-Stats",
        20: "Bundesliga-Stats",
        9: "Premier-League-Stats",
        12: "La-Liga-Stats"
    } 
  
    # get() method of dictionary data type returns  
    # value of passed argument if it is present  
    # in dictionary otherwise second argument will 
    # be assigned as default value of passed argument 
    return switcher.get(argument) 


@app.route('/<int:numberOfLeague>/<string:types>')
def get_data_by_league(numberOfLeague, types):
    league = get_league_by_number(numberOfLeague)
    chrome_options = Options()
    chrome_options.headless = True
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--log-level=3")
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    browser = webdriver.Chrome('C:\\Users\\mouis\\webDriver\\chromedriver', options=chrome_options)
    link = 'https://fbref.com/en/comps/{}/'+types+'/'+league
    link = link.format(numberOfLeague)
    browser.get(link)
    if types == 'stats': types = 'standard'
    if types == 'keepers': types = 'keeper'
    elem1 = browser.find_element(
    By.XPATH, '//*[@id="all_stats_'+types+'_squads"]/div[1]/div/ul/li[1]')
    elem1.click()
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="all_stats_'+types+'_squads"]/div[1]/div/ul/li[1]/div/ul/li[4]/button'))).click()
    csv1 = browser.find_element(By.XPATH, '//*[@id="csv_stats_'+types+'_squads"]')
    response1 = csv1.text
    response1 = response1.replace(",", ";")
    if types == "shooting":
       response1 = response1.split("\n",1)[1];
    else : response1 = response1.split("\n",2)[2];
    elem = browser.find_element(
    By.XPATH, '//*[@id="all_stats_'+types+'"]/div[1]/div/ul/li[1]')
    elem.click()
    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="all_stats_'+types+'"]/div[1]/div/ul/li[1]/div/ul/li[4]/button'))).click()
    csv = browser.find_element(By.XPATH, '//*[@id="csv_stats_'+types+'"]')
    response = csv.text
    response = response.replace(",", ";")
    if types == "shooting":
       response = response.split("\n",1)[1];
    else : response = response.split("\n",2)[2];
    browser.close()
    browser.quit()
    return response1

@app.route('/all')
def get_all_data():
    data = {}
    chrome_options = Options()
    chrome_options.headless = True
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
    browser = webdriver.Chrome('C:\\Users\\mouis\\webDriver\\chromedriver', options=chrome_options)
    browser.implicitly_wait(10)
    # browser.set_page_load_timeout(5)            
    for competition in competitions:
        item = {}
        for typ in types:
            league = get_league_by_number(competition)         
            tosh = "l'identifiant' : {}"
            tosh = tosh.format(competition)
            print(tosh)
            print('la competition : '+league)           
            link = 'https://fbref.com/en/comps/{}/'+typ+'/'+league
            link = link.format(competition)
            print(link)
            browser.get(link)
            if typ == 'stats': typ = 'standard'
            if typ == 'playingtime': typ = 'playing_time'
            if typ == 'keepers': typ = 'keeper'
            if typ == 'keepersadv': typ = 'keeper_adv'
            print("le type : "+typ)
#Scapping the squad's datas       
            try:
                elem1 = WebDriverWait(browser, 300, poll_frequency=10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="all_stats_'+typ+'_squads"]/div[1]/div/ul/li[1]'))
                )
            finally:
                elem1.click()
                try:
                    getCsvButton1 = WebDriverWait(browser, 300, poll_frequency=10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="all_stats_'+typ+'_squads"]/div[1]/div/ul/li[1]/div/ul/li[4]/button')))
                    getCsvButton1.click()
                finally:    
                    csv = browser.find_element(By.XPATH, '//*[@id="csv_stats_'+typ+'_squads"]')
                    responseForSqaud = csv.text
                    responseForSqaud = responseForSqaud.replace(",", ";")
                    if typ == "shooting": responseForSqaud = responseForSqaud.split("\n",1)[1]  
                    else : responseForSqaud = responseForSqaud.split("\n",2)[2]      
                    item['squad '+typ] = responseForSqaud 
#Scapping the players's datas
            try:
                elem = WebDriverWait(browser, 300, poll_frequency=10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="all_stats_'+typ+'"]/div[1]/div/ul/li[1]'))
                )
            finally:
                elem.click()
                try:
                    getCsvButton = WebDriverWait(browser, 300, poll_frequency=10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="all_stats_'+typ+'"]/div[1]/div/ul/li[1]/div/ul/li[4]/button')))
                    getCsvButton.click()
                finally:    
                    csv = browser.find_element(By.XPATH, '//*[@id="csv_stats_'+typ+'"]')
                    print('________________________________________________')
                    response = csv.text
                    response = response.replace(",", ";")
                    if typ == "shooting":  response = response.split("\n",1)[1]          
                    else : response = response.split("\n",2)[2]       
                    key = league+'-'+typ 
                    item[typ] = response      
            data[league] = item    
        return data
        break  
    return data    
    browser.close()
    browser.quit()
app.run(port=5000)
