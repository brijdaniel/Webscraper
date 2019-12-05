"""
Generate https://www.realestate.com.au/* URL's to scrape
"""

import pandas


def create_url_list(search_type):
    """
    Creates list of URL's in www.realestate.com.au format to search for any of rent, buy  or sold properties in the
    list of Adelaide suburbs. Note the returned URL's have the page number missing at the end, so this can be added
    on iteratively later.

    :param search_type: String representing desired URL search type, one of sold, rent or buy
    :return: List of URLs with page number missing
    """

    # Read in csv file as pandas series
    suburbs = pandas.read_csv('list_of_adelaide_suburbs.csv', index_col=False)
    suburb_list = suburbs['Suburb']

    url_base = 'https://www.realestate.com.au/'
    url_list = []

    # Iterate through list of suburbs, replace spaces with + and generate URL format
    for suburb in suburb_list:
        suburb = suburb.replace(' ', '+')
        combined_url = url_base + search_type +'/in-' +  suburb + ',+sa/list-'
        url_list.append(combined_url)

    return  url_list


l = create_url_list('sold')
print(l)