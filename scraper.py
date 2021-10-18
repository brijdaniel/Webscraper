"""
Web scraper engine to extract source html for input to html_parser().
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
#from fake_useragent import UserAgent


class Scraper:
    def __init__(self):
        """
        Initialise a Scraper instance using chromedriver. This scraper uses UserAgent to generate random, but valid,
        user agents for each instance.
        """

        # Set up random fake user agent
        # ua = UserAgent()
        # user_agent = ua.random

        # Set up basic firefox profile
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        #chrome_options.add_argument(f'user-agent={user_agent}')
        chrome_options.add_argument("start-maximized")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        caps = chrome_options.to_capabilities()

        # Load chrome driver
        self.driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options, desired_capabilities=caps)

    def scrape(self, url):
        """
        Navigate to desired URL and return source HTML.

        :param url: URL to scrape source HTML from
        :return: Source HTML of web page
        """

        # Make GET request TODO need to catch timeout exception and wait until wifi reconnects before resuming
        self.driver.get(url)
        
        # Wait for data to load
        WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.CLASS_NAME, "divided-content")))
        
        # Get source HTML
        source_html = self.driver.page_source

        # Return source HTML
        return source_html

    def close(self):
        """
        Close browser instance.
        :return: None
        """

        # Close headless browser
        self.driver.quit()
