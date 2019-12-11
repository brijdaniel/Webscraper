"""
Web scraper engine to extract source html for input to html_parser().
"""

from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def scrape(url):
    """
    Uses geckodriver/firefox combo to load web page and extract source HTML.

    :param url: URL to scrape source HTML from
    :return: Source HTML of web page
    """

    # Set up basic firefox profile
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override","Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:71.0) Gecko/20100101 Firefox/70.0")
    profile.set_preference("browser.privatebrowsing.autostart", True)
    profile.update_preferences()

    # Load geckodriver for firefox. Requires geckodriver current working directory
    firefox_options = Options()
    firefox_options.add_argument('--headless')
    driver = webdriver.Firefox(firefox_options=firefox_options, executable_path='./geckodriver.exe', firefox_profile=profile)

    # Make GET request
    driver.get(url)
    sleep(5)  # TODO put wait in here to wait for page to load

    # Get source HTML
    source_html = driver.page_source

    # Close headless browser
    driver.quit()

    # Return source HTML
    return  source_html
