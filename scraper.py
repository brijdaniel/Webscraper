"""
Web scraper engine to extract source html for input to html_parser().
This all needs to be put into a class and broken down into methods... but for now this will do for testing

Sorry @Ben this is where it gets fucked lel.
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def scrape(url):
    # Stuff to bypass bot detenction, not currently used
    user_agents = ['Googlebot/2.1', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0']
    proxies = {'http': '208.98.185.89:53630',
               'https': '208.98.185.89:53630'}

    # URL collection
    base_url = 'https://www.realestate.com.au'
    search_url = 'https://www.realestate.com.au/sold/in-henley+beach/list-1'
    wmb_url = 'https://www.whatsmybrowser.org/'

    # Set up basic (very basic!) firefox profile
    # Have tried to load my actual firefox profile in here but its super slow and usually crashes, suspected memory leak
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override","Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0")
    profile.set_preference("browser.privatebrowsing.autostart", True)
    #profile.set_preference("javascript.enabled", False)
    profile.update_preferences()

    # Load geckodriver for firefox. Requires geckodriver current working directory
    firefox_options = Options()
    #firefox_options.add_argument('--headless')
    driver = webdriver.Firefox(firefox_options=firefox_options, executable_path='./geckodriver.exe', firefox_profile=profile)  # webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe', chrome_options=chrome_options)

    # Make GET request!!
    driver.get(url)

    # after the URL, this is the js that comes up just before a successful connection
    #driver.execute_script("https://www.realestate.com.au/149e9513-01fa-4fb0-aad4-566afd725d1b/2d206a39-8ed7-437e-a3be-862e0f06eea3/fingerprint/script/kpf.js?url=/149e9513-01fa-4fb0-aad4-566afd725d1b/2d206a39-8ed7-437e-a3be-862e0f06eea3/fingerprint&amp;token=4d4891a1-fa6e-09c9-767a-545bfd1bd4f2")

    # === Search from home page approach ===
    # This code navigates to the realestate.com.au homepage, then types in the search bar and searches manually
    # Still unable to load the serach results though :(
    driver.get(base_url)  # Load homepage
    WebDriverWait(driver, 10)  # Wait 10s for some content to load
    driver.find_element_by_link_text('Sold').click()  # Find the Sold link and click on it
    WebDriverWait(driver, 10) # Wait 10s for some content to load
    driver.execute_script("document.getElementById('where').setAttribute('value', 'Henley Beach')")  # Use javascript to fill out form
    button = driver.find_element_by_class_name('rui-search-button')  # Find search button
    WebDriverWait(driver, 2)  # Wait a cuttla
    button.click()
    WebDriverWait(driver, 10) # Wait 10s for some content to load


    # Get html source, when all this works then this would be the returned value to html_parser()
    html_source = BeautifulSoup(driver.page_source, 'html.parser')
    return  html_source
