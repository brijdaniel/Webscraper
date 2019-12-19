from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent

url = 'https://www.realestate.com.au/sold/in-auldana,+sa+5072/list-2'
js_url = 'https://www.realestate.com.au/sold/public/vendors-185f85cdf9cc12aeeeed.js'

# Set up random fake user agent
ua = UserAgent()
user_agent = ua.random

# Set up basic firefox profile
chrome_options = Options()
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("start-maximized")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
#chrome_options.add_argument('--headless')

caps = chrome_options.to_capabilities()

# Load chrome driver
driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options, desired_capabilities=caps)

# Make GET request
driver.get(url)
#driver.execute_script('return document.readyState')
# 'tiered-results tiered results--exact'

sleep(5)

# Get source HTML
html = driver.page_source

# Close headless browser
#driver.quit()

print(html)