from bs4 import BeautifulSoup
import requests

url = 'https://www.realestate.com.au/sold/public/main-34ba6154799f06fb7c72.js'

response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'})
content = BeautifulSoup(response.content, 'html.parser')

print(content)