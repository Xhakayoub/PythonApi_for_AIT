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
import curses
import sys
import time



app = Flask(__name__)
linkControlls = {
    "keeper" : { "liPosition" : '3', "secondLiPosition" : '3', "divPosition" : '1', "secondDivPosition" : '1'},
    "keeper_adv" : { "liPosition" : '2', "secondLiPosition" : '2', "divPosition" : '1', "secondDivPosition" : '1'},
    "standard" : { "liPosition" : '2', "secondLiPosition" : '2', "divPosition" : '2', "secondDivPosition" : '1'},
    "passing" : { "liPosition" : '2', "secondLiPosition" : '2', "divPosition" : '2', "secondDivPosition" : '1'},
    "shooting" : { "liPosition" : '2', "secondLiPosition" : '2', "divPosition" : '2', "secondDivPosition" : '1'},
    "playing_time" : { "liPosition" : '2', "secondLiPosition" : '2', "divPosition" : '2', "secondDivPosition" : '1'},
    "misc" : { "liPosition" : '2', "secondLiPosition" : '2', "divPosition" : '2', "secondDivPosition" : '1'},
    "passing_types" : { "liPosition" : '2', "secondLiPosition" : '2', "divPosition" : '2', "secondDivPosition" : '1'},
    "defense" : { "liPosition" : '2', "secondLiPosition" : '2', "divPosition" : '2', "secondDivPosition" : '1'},
    "possession" : { "liPosition" : '2', "secondLiPosition" : '2', "divPosition" : '2', "secondDivPosition" : '2'}
}
types = [ 'passing_types', 'possession','keepers', 'stats', 'passing', 'shooting', 'playingtime', 'keepersadv', 'misc', 'defense']
competitions = [19]#, 13, 8, 9, 12, 20, 11] 
checkKeeper = ['keeper', 'keeper_adv']

def checkFirstLine(firstLine):
    arraychecker = ['---']
    boolean = False
    # print("line is " +firstLine)
    if any(x in firstLine for x in arraychecker) :
       boolean = True
    if not firstLine.strip():  
    #    print("empty line")
       boolean = True
    return boolean

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
    browser = webdriver.Chrome('/home/amouissi/Documents/projects/AITransfert/chromedriver', options=chrome_options)
    # browser.set_page_load_timeout(5)    
    browser.set_window_size(3840, 2160)

    # print('________________________________________')
    # i = 0
    for competition in competitions:
        item = {}
        for typ in types:
            league = get_league_by_number(competition)  
            tosh = "l'identifiant' : {}"
            tosh = tosh.format(competition)
            liPosition = '2'
            secondLiPosition = '1'
            divPosition = '1'
            if league == 'Champions-League-Stats' or league == 'Europa-League-Stats' :      
                liPosition = '3'
                secondLiPosition = '2'
            # print(tosh)
            print('la competition : '+league)           
            link = 'https://fbref.com/en/comps/{}/'+typ+'/'+league
            link = link.format(competition)
            print(link)
            browser.get(link)
            if typ == 'stats': typ = 'standard'
            if typ == 'playingtime': typ = 'playing_time'
            if typ == 'keepers': 
                typ = 'keeper' 
                liPosition = '3'
                secondLiPosition = '3'
                if league == 'Champions-League-Stats'  :
                     liPosition = '4'
                     secondLiPosition = '3'               
            if typ == 'keepersadv': typ = 'keeper_adv'
            # print("le type : "+typ)
#Scrapping the squad's datas 
            # print(testConnection.test_connection()) 
            while testConnection.test_connection() == False :
                print('Waiting for internet ....')
                time.sleep(5)
            try: 
                liPos = '0'
                checktext = ''
                while checktext != 'Share & Export' :
                    liPos = str(int(liPos) + 1)
                    checktext = browser.find_element(By.XPATH,'//*[@id="stats_squads_'+typ+'_for_sh"]/div/ul/li['+liPos+']').text     
                    # print(checktext + ' - ' + liPos)
                # xpath = '//*[@id="stats_squads_'+typ+'_for_sh"]/div/ul/li['+liPos+']/span'
                # print(xpath)
                elem1 = WebDriverWait(browser, 10, poll_frequency=2).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="stats_squads_'+typ+'_for_sh"]/div/ul/li['+liPos+']/span'))
                )
                ActionChains(browser).move_to_element(elem1).perform()
            finally:
                try:
                    # print('//*[@id="stats_squads_'+typ+'_for_sh"]/div/ul/li['+liPos+']/div/ul/li[4]/button')
                    getCsvButton1 = WebDriverWait(browser, 10, poll_frequency=2).until(
                        EC.presence_of_element_located((By.XPATH, 
                        '//*[@id="stats_squads_'+typ+'_for_sh"]/div/ul/li['+liPos+']/div/ul/li[4]/button')))
                    # print('located')
                    getCsvButton1 = WebDriverWait(browser, 10, poll_frequency=2).until(
                        EC.element_to_be_clickable((By.XPATH,
                        '//*[@id="stats_squads_'+typ+'_for_sh"]/div/ul/li['+liPos+']/div/ul/li[4]/button')))
                except TimeoutException : 
                     print("Loading took too much time!")    
                finally:
                    browser.execute_script("arguments[0].click();", getCsvButton1)     
                    # getCsvButton1.click()
                    # print('clicked')#//*[@id="csv_stats_squads_keeper_for"]/text()[2]
                    element1 = WebDriverWait(browser, 10, poll_frequency=2).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="csv_stats_squads_'+typ+'_for"]')))
                    csv = browser.find_element(By.XPATH, '//*[@id="csv_stats_squads_'+typ+'_for"]')
                    responseForSqaud = csv.text
                    responseForSqaud = responseForSqaud.replace(",", ";")
                    textForLoop = responseForSqaud
                    j = 0
                    # firstLine = csv.text.readlines()[j]
                    # print(len(textForLoop.split("\n")))
                    for itemm in textForLoop.split("\n"):
                        #print(checkFirstLine(itemm))
                        if checkFirstLine(itemm) == True :
                            # print('fisrt line is line number '+ str(j))  
                            j = j + 1
                            # firstLine = responseForSqaud.readlines()[j]
                        else : break  
                    if typ == "shooting" or typ == "passsing_types": responseForSqaud = responseForSqaud.split("\n",j)[j]  
                    else : responseForSqaud = responseForSqaud.split("\n",j)[j]   
                    print('fisrt line is line number '+ str(j))  
                    item['squad '+typ] = responseForSqaud 
                    
#Scapping the players's datas
            # print(testConnection.test_connection()) 
            while testConnection.test_connection() == False :
                print('Waiting for internet ....')
                time.sleep(5)
            try:
                if competition == 19 and typ not in checkKeeper : 
                        secondLiPosition = '2'
                        divPosition = '2'
                        #//*[@id="stats_keeper"]/div[1]/div/ul/li[3]/span
                        collpaseButton =  WebDriverWait(browser, 10, poll_frequency=2).until(
                        EC.element_to_be_clickable((By.XPATH,
                        '//*[@id="stats_'+typ+'_control"]')))
                        browser.execute_script("arguments[0].click();", collpaseButton)  
                        print('Collapse Button Clicked')   
                liPos = '0'
                checktext = ''
                while checktext != 'Share & Export' :
                    liPos = str(int(liPos) + 1) 
                    checktext = browser.find_element(By.XPATH,'//*[@id="stats_'+typ+'_sh"]/div/ul/li['+liPos+']').text
                    print(checktext + ' - ' + liPos)
                print('//*[@id="stats_'+typ+'_sh"]/div/ul/li['+liPos+']/span')
                elem = WebDriverWait(browser, 10, poll_frequency=2).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="stats_'+typ+'_sh"]/div/ul/li['+liPos+']/span'))
                )
            finally:   
                ActionChains(browser).move_to_element(elem).perform()
                try:
                    getCsvButton = WebDriverWait(browser, 10, poll_frequency=2).until(
                        EC.presence_of_element_located((By.XPATH,
                            '//*[@id="stats_'+typ+'_sh"]/div/ul/li['+liPos+']/div/ul/li[4]/button')))
                    print('located')
                    getCsvButton = WebDriverWait(browser, 10, poll_frequency=2).until(
                        EC.element_to_be_clickable((By.XPATH, 
                        '//*[@id="stats_'+typ+'_sh"]/div/ul/li['+liPos+']/div/ul/li[4]/button')))  
                except TimeoutException : 
                    print("Loading took too much time!")
                finally:   
                    browser.execute_script("arguments[0].click();", getCsvButton) 
                    # getCsvButton.click()
                    print('clicked')
                    element = WebDriverWait(browser, 10, poll_frequency=2).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="csv_stats_'+typ+'"]')))
                    csv = browser.find_element(By.XPATH, '//*[@id="csv_stats_'+typ+'"]')
                    print('________________________________________________')
                    response = csv.text
                    response = response.replace(",", ";")
                    j = 0
                    textForLoop = response
                    for itemm in textForLoop.split("\n"):
                        #print(checkFirstLine(itemm))
                        if checkFirstLine(itemm) == True :
                            # print('fisrt line is line number '+ str(j))  
                            j = j + 1
                            # firstLine = responseForSqaud.readlines()[j]
                        else : break    
                    if typ == "shooting" or typ == "passsing_types":  response = response.split("\n",j)[j]          
                    else : response = response.split("\n",j)[j]       
                    key = league+'-'+typ 
                    item[typ] = response      
            # else : print('No internet') 
            data[league] = item    
    return data    

    browser.close()
    browser.quit()
app.run(port=5000)


# @app.route('/<int:numberOfLeague>/<string:types>')
# def get_data_by_league(numberOfLeague, types):
#     league = get_league_by_number(numberOfLeague)
#     chrome_options = Options()
#     chrome_options.headless = True
#     chrome_options.add_argument('--disable-gpu')
#     chrome_options.add_argument("--log-level=3")
#     # chrome_options.add_argument("--headless")
#     # chrome_options.add_argument('--disable-gpu')  # Last I checked this was necessary.
#     browser = webdriver.Chrome('C:\\wamp64\\www\\chromedriver', options=chrome_options)
#     link = 'https://fbref.com/en/comps/{}/'+types+'/'+league
#     link = link.format(numberOfLeague)
#     browser.get(link)
#     if types == 'stats': types = 'standard'
#     if types == 'keepers': types = 'keeper'
#     elem1 = browser.find_element(
#     By.XPATH, '//*[@id="all_stats_'+types+'_squads"]/div[1]/div/ul/li[1]')
#     elem1.click()
#     WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="all_stats_'+types+'_squads"]/div[1]/div/ul/li[1]/div/ul/li[4]/button'))).click()
#     csv1 = browser.find_element(By.XPATH, '//*[@id="csv_stats_'+types+'_squads"]')
#     response1 = csv1.text
#     response1 = response1.replace(",", ";")
#     if types == "shooting":
#        response1 = response1.split("\n",1)[1];
#     else : response1 = response1.split("\n",2)[2];
#     elem = browser.find_element(
#     By.XPATH, '//*[@id="all_stats_'+types+'"]/div[1]/div/ul/li[1]')
#     elem.click()
#     WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="all_stats_'+types+'"]/div[1]/div/ul/li[1]/div/ul/li[4]/button'))).click()
#     csv = browser.find_element(By.XPATH, '//*[@id="csv_stats_'+types+'"]')
#     response = csv.text
#     response = response.replace(",", ";")
#     if types == "shooting" or types == "passsing_types":
#        response = response.split("\n",1)[1];
#     else : response = response.split("\n",2)[2];
#     browser.close()
#     browser.quit()
#     return response1
