"""
Web scraper engine to extract source html for input to html_parser().
"""
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent


def scrape(url):
    """
    Uses geckodriver/firefox combo to load web page and extract source HTML.

    :param url: URL to scrape source HTML from
    :return: Source HTML of web page
    """

    # Set up random fake user agent
    ua = UserAgent()
    user_agent = ua.random

    # Set up basic firefox profile
    chrome_options = Options()
    chrome_options.add_argument(f'user-agent={user_agent}')
    chrome_options.add_argument("start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    # chrome_options.add_argument('--headless')

    caps = chrome_options.to_capabilities()

    # Load chrome driver
    driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options, desired_capabilities=caps)

    # Make GET request
    driver.get(url)
    # 'tiered-results tiered results--exact'
    sleep(5)

    # Get source HTML
    source_html = driver.page_source

    # Close headless browser
    driver.quit()

    # Return source HTML
    return source_html
