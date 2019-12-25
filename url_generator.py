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
        combined_url = url_base + search_type + '/in-' + suburb + ',+sa/list-'
        url_list.append(combined_url)

    return url_list


def filter_list(url_list, log_date_tuple):
    """
    Takes in list from create_url_list and filters against the log file from a previous scraping run. Returns a
    filtered list of URLs of suburbs which haven't been fully scraped.

    :param url_list: List output from create_url_list()
    :param log_date_tuple: Tuple of log file names to filter URLs against
    :return: Filtered list of URLs
    """

    # Unpack tuple into single dataframe
    log_df = pandas.DataFrame()
    for log in log_date_tuple:
        log_data = pandas.read_excel('Logs/' + log)
        log_df = log_df.append(log_data)

    # Filter down to suburbs that had a successful 50th page, ie have been completely scraped
    log_df = log_df[log_df['Page']==50]

    # Get the URLs of these suburbs
    url_to_filter = list(log_df['URL'])

    # Filter the input URL list
    filtered_urls = [url for url in url_list if url not in url_to_filter]

    return filtered_urls
