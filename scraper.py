from time import sleep

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# To bypass bot detenction, not currently used
user_agents = ['Googlebot/2.1', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0']
proxies = {'http': '208.98.185.89:53630',
           'https': '208.98.185.89:53630'}

base_url = 'https://www.realestate.com.au'
search_url = 'https://www.realestate.com.au/sold/in-henley+beach/list-1'
wmb_url = 'https://www.whatsmybrowser.org/'

profile = webdriver.FirefoxProfile()
profile.set_preference("general.useragent.override","Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0")
profile.set_preference("browser.privatebrowsing.autostart", True)
#profile.set_preference("javascript.enabled", False)
profile.update_preferences()

# Load geckodriver for firefox. Assumes geckodriver is in current path
firefox_options = Options()
#firefox_options.add_argument('--headless')
#chrome_options.binary_location = './chromedriver.exe'
driver = webdriver.Firefox(firefox_options=firefox_options, executable_path='./geckodriver.exe', firefox_profile=profile)  # webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe', chrome_options=chrome_options)

#cookie =

driver.get(search_url)

# Load webpage
"""
driver.get(search_url)
#driver.add_cookie('{"t":"8ec7b5e9-7933-3f1f-18a5-e28ac246b939","d":{"a7338e2668bdc2c62b37d5012d56c51a83da50f323283b6dc0414438eb81b0727":"0db3c4cbe6d18e74aff628fb8f2429b6","aae914232bc2f0da229016bdc3d801ee7fc62bd6bc2e4e2fc6fb6af6eb183cf74":"Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0","a9e4b6cf51124a7d1d1b88e330007a9e11b936cfad33985311e6d364db9575388":false,"abed7cbb55549b4081bf2d304532f4edfe1319a2eba8356fd92902c6ded827c78":false,"a4ac87cf6233e812cefb6182233a24bdb113dba459a9aaebfcfae463674cdfe80":false,"a459f978d7eaa9a8b83b273a19b1a1077900600ec84309d90d47fa83db526e096":true,"a98acb9bc3f2d732e9cfd373321008cb0abed83d1451395056a2363ebf668c3e3":[1408,792],"a48090f8e4d92813d4fa563da01af4ab9927045434b579ffcb4f7a6acd56aa50c":["Shockwave Flash::Shockwave Flash 32.0 r0::application/x-shockwave-flash~swf,application/futuresplash~spl"],"abe1185a010b9eee286955ba78363dec1276def93f871d64aded1b140ba220b3e":[],"a150e2bb2da775c5c859ef434d020675743e7b27e905538110e3622adc533fae6":"_0x267231@https://www.realestate.com.au/149e9513-01fa-4fb0-aad4-566afd725d1b/2d206a39-8ed7-437e-a3be-862e0f06eea3/fingerprint/script/kpf.js?url=/149e9513-01fa-4fb0-aad4-566afd725d1b/2d206a39-8ed7-437e-a3be-862e0f06eea3/fingerprint&token=8ec7b5e9-7933-3f1f-18a5-e28ac246b939:1:14791\n_0x477b8b@https://www.realestate.com.au/149e9513-01fa-4fb0-aad4-566afd725d1b/2d206a39-8ed7-437e-a3be-862e0f06eea3/fingerprint/script/kpf.js?url=/149e9513-01fa-4fb0-aad4-566afd725d1b/2d206a39-8ed7-437e-a3be-862e0f06eea3/fingerprint&token=8ec7b5e9-7933-3f1f-18a5-e28ac246b939:1:19164\n_0x214bbb/<@https://www.realestate.com.au/149e9513-01fa-4fb0-aad4-566afd725d1b/2d206a39-8ed7-437e-a3be-862e0f06eea3/fingerprint/script/kpf.js?url=/149e9513-01fa-4fb0-aad4-566afd725d1b/2d206a39-8ed7-437e-a3be-862e0f06eea3/fingerprint&token=8ec7b5e9-7933-3f1f-18a5-e28ac246b939:1:22268\nget/<@https://www.realestate.com.au/149e9513-01fa-4fb0-aad4-566afd725d1b/2d206a39-8ed7-437e-a3be-862e0f06eea3/f.js:1:1802\njsFontsKey/<@https://www.realestate.com.au/149e9513-01fa-4fb0-aad4-566afd725d1b/2d206a39-8ed7-437e-a3be-862e0f06eea3/f.js:1:14149\n","a8560c24c688dad0930e11382134f61c54362e3ca54f24a1b4cefc2d5e5320500":false,"ad26fc2ad544555b4fad01e69bb4ec3d9c435c206f0043c284be945a6e74379c4":false,"ac626b621b5ead0b0b3fb15bcce23563778fec6561b4c41f5ca66e6da4d03e512":false,"a3acf501298e45668114448d2fd98a379a6fddafe2b83b3bef6029e4a9012aaf2":false,"a2cd38277797c54ed91c99b8e7a4035b19d1753e7ae78fdf5fea6637ed2d25c4d":false}}')
driver.get('https://tags.tiqcdn.com/utag/rea-group/main/prod/utag.js')
WebDriverWait(driver, 1)
driver.get('https://www.realestate.com.au/sold/public/main-e4001e88b05d91bc4aa2.js')
WebDriverWait(driver, 1)
driver.get('https://www.realestate.com.au/sold/public/finx-0a7e0800ab377c6eb466.js')
WebDriverWait(driver, 1)
driver.get('https://www.realestate.com.au/sold/public/vendors-4b6ecdb2b76d0162420f.js')
WebDriverWait(driver, 1)
driver.get(search_url)
"""

# after the URL, this is the js that comes up just before a successful connection
#driver.execute_script("https://www.realestate.com.au/149e9513-01fa-4fb0-aad4-566afd725d1b/2d206a39-8ed7-437e-a3be-862e0f06eea3/fingerprint/script/kpf.js?url=/149e9513-01fa-4fb0-aad4-566afd725d1b/2d206a39-8ed7-437e-a3be-862e0f06eea3/fingerprint&amp;token=4d4891a1-fa6e-09c9-767a-545bfd1bd4f2")

"""
# Navigate around page, search for what we want
WebDriverWait(driver, 10)  # Wait 10s for some content to load
#WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID,"LOCSTORAGE")))
#WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//span[@id='HRS_APPL_WRK_HRS_PAGE_TITLE']")))
driver.find_element_by_link_text('Sold').click()  # Find the Sold link and click on it
WebDriverWait(driver, 10) # Wait 10s for some content to load
driver.execute_script("document.getElementById('where').setAttribute('value', 'Henley Beach')")  # Use javascript to fill out form
button = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[1]/form/div/div[1]/div/div/button')
WebDriverWait(driver, 2)
button.click()
#driver.execute_async_script('javascript/blocked')
#driver.execute_script("https://www.realestate.com.au/149e9513-01fa-4fb0-aad4-566afd725d1b/2d206a39-8ed7-437e-a3be-862e0f06eea3/fingerprint/script/kpf.js?url=/149e9513-01fa-4fb0-aad4-566afd725d1b/2d206a39-8ed7-437e-a3be-862e0f06eea3/fingerprint&amp;token=4d4891a1-fa6e-09c9-767a-545bfd1bd4f2")
WebDriverWait(driver, 10) # Wait 10s for some content to load
"""


html_source = BeautifulSoup(driver.page_source, 'html.parser')
print(html_source)

# Find elements
#results = driver.find_elements_by_class_name("property-price ")
#driver.quit()

#print(len(results))
#print(results)



"""
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'})
content = BeautifulSoup(response.content, 'html.parser')

price = content.find_all('span', attrs={'class':'property-price '})

print(price)
"""