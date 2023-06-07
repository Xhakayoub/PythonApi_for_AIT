import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

@pytest.mark.slow
def test_example():
    # Initialise le navigateur
    chrome_options = Options()
    chrome_options.headless = True
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("enable-automation")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.page_load_strategy = 'none'
    driver = webdriver.Chrome('/home/amouissi/Documents/projects/AITransfert/chromedriver', options=chrome_options)

    # Charge une page web
    driver.get('https://fbref.com/en/comps/9/Premier-League-Stats')

    # Exécute des actions sur la page
    element = driver.find_element(By.XPATH ,'//*[@id="meta"]/div[2]/h1')  # Trouve l'élément de recherche 


    # Vérifie le résultat
    assert "Premier League Stats | FBref.com" == driver.title

    # Ferme le navigateur
    driver.quit()