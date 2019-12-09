"""
Main interface for executing webscraper and building SQLite database.
"""
import datetime
import os
import multiprocessing
import pandas
from sqlalchemy.exc import IntegrityError
import html_parser, database_models, scraper, url_generator


class CacheComplete:
    def __init__(self):
        self.cache_df = pandas.DataFrame(columns=['URL', 'Suburb', 'Page', 'Status', 'Timestamp'])

    def append(self, data):
        self.cache_df = self.cache_df.append(data, index=False)

    def export(self):
        os.makedirs('Caches', exist_ok=True)
        cache_path = os.path.join('Caches', str(datetime.datetime.today()) + '.xlsx')
        self.cache_df.to_excel(cache_path, index=False)


def gather_data(suburb_url, cache_object):
    # Unpack suburb from URL for debugging, probably a nicer way to do this
    suburb = (suburb_url.split('in-')[1]).split(',')[0]

    # Iterate through 50 pages of search results
    # TODO changed this from 50 to 3 just for debugging, change back !!!
    for page in range(1, 3 + 1):
        # URL to scrape
        url = suburb_url + str(page)

        print('Scraping page ' + str(page) + ' of ' + suburb + ' at ' + str(datetime.datetime.now()))

        # Get URL source HTML
        source_html = scraper.scrape(url)

        # Parse data
        parser = html_parser.HTMLParser(source_html)
        property_df, sold_df = parser.parse_data('sold')

        # Data to send to cache
        cache_data = {'URL': suburb_url,
                      'Suburb': suburb,
                      'Page': page,
                      'Timestamp': datetime.datetime.now()}
        if not property_df.empty or sold_df.empty:
            cache_data['Status'] = 'Successful'
        else:
            cache_data['Status'] = 'Failed'
        cache_object.append(cache_data)

        return property_df, sold_df


def build_database(db_session, property_df, secondary_df, *args):
    # Select SQL table to append to based on *args
    if 'sold' in args:
        table_name = 'Sold History'
    elif 'rent' in args:
        table_name = 'Rent History'
    # TODO add other cases. Should an exception here if no valid case is given

    # Add dataframe to database
    # TODO below line fails when duplicate entries occur, hence iterate through df
    #  manually which is slow...
    #  sold_properties_df.to_sql('Sold Property', con=engine, if_exists='append', index=False)
    #  Optimise below code later on
    for i in range(len(property_df)):
        try:
            property_df.iloc[i:i+1].to_sql(name='Property', if_exists='append', con=db_session.engine, index=False)
        except IntegrityError:
            pass

    for x in range(len(secondary_df)):
        try:
            secondary_df.iloc[x:x+1].to_sql(name=table_name, if_exists='append', con=db_session.engine, index=False)
        except IntegrityError:
            pass


if __name__ == '__main__':
    # Get list of sold suburb URLs
    url_list = url_generator.create_url_list('sold')

    # Chop off suburbs we have done previously
    url_list = url_list[:4]

    # Create cache object
    cache = CacheComplete()

    # Create session for SQLite database
    database_name = 'realestate_database.db'
    db = database_models.Database(database_name=database_name)

    try:
        # Map list of URLs to max number of processes, execute build database
        # This will go through the list sequentially, rather than randomly
        with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
            property_results, sold_results = pool.map(gather_data, url_list)

        # Concatenate list of df results into single df
        property_df = pandas.concat(property_results)
        sold_df = pandas.concat(sold_results)

        # Append dataframes to database
        build_database(db, property_df, sold_df, 'sold')

        # Kill database session
        db.engine.dispose()

        # Export completed data to cache file
        cache.export()

    # If something fails, save the data we have
    # TODO not sure if this will actually work. If an exception is raised during the multiprocessing,
    #  will the contents of *_results survive through to this finally??
    finally:
        # Concatenate list of df results into single df
        property_df = pandas.concat(property_results)
        sold_df = pandas.concat(sold_results)

        # Append dataframes to database
        build_database(db, property_df, sold_df, 'sold')

        # Kill database session
        db.engine.dispose()

        # Make sure cache file is still created if process fails
        cache.export()








    # TODO Got up to Beverley (43 in list), half of Hectorville needs doing, as well as Adelaide and North Adelaide
    #  stopped at Forestille, Marlseton, Fullarton, Mile End
    #  Error at Walkerville selenium.common.exceptions.WebDriverException: Message: Reached error page: about:neterror?e=dnsNotFound&u=https%3A//www.realestate.com.au/sold/in-Elizabeth+Downs%2C+sa/list-39&c=UTF-8&f=regular&d=We%20can%E2%80%99t%20connect%20to%20the%20server%20at%20www.realestate.com.au.
    #  selenium.common.exceptions.WebDriverException: Message: Reached error page: about:neterror?e=dnsNotFound&u=https%3A//www.realestate.com.au/sold/in-Elizabeth+Downs%2C+sa/list-39&c=UTF-8&f=regular&d=We%20can%E2%80%99t%20connect%20to%20the%20server%20at%20www.realestate.com.au.
