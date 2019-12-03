Webscraper

Currently the html parsing side works, and the main.py module can be used to parse html and populate a SQLite database, but the source html must be downloaded and stored locally in the working directory.

The scraper side of things doesn't work... yet. Recommend running request_scraper.py first to see the initial basic response from the server to the GET request. Then look at scraper.py, which uses Selenium and geckodriver+firefox to try to interact and receive actual content.

Good luck!
