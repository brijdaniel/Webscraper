"""
Quick script to scrape list of Adelaide suburbs from wikipedia
"""

import pandas

if __name__ == '__main__':
    url = 'https://en.wikipedia.org/wiki/List_of_Adelaide_suburbs'

    # Get table from wiki page with awesome pandas function (returns list of DFs)
    table = pandas.read_html(url)

    # Get Suburb column from first df
    suburbs = table[0]['Suburb']

    # Output list of suburbs to csv file
    suburbs.to_csv('./list_of_adelaide_suburbs', index=False)
