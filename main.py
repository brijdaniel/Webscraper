"""
Main interface for executing webscraper and building SQLite database.
"""
import time
import datetime
import os
import multiprocessing
from itertools import repeat
import pandas
from sqlalchemy.exc import IntegrityError
import html_parser, database_models, scraper, url_generator


def gather_data(suburb_url, data_type, property_cache, secondary_cache, log_cache):
    # TODO sold_cache should really be secondary_cache, and there should be another arg for data_type='sold'

    # Unpack suburb from URL for debugging, probably a nicer way to do this
    suburb = (suburb_url.split('in-')[1]).split(',')[0]

    # Create scraper instance, ie open browser
    browser = scraper.Scraper()

    # Iterate through 50 pages of search results
    for page in range(1, 50 + 1):
        # URL to scrape
        url = suburb_url + str(page)

        print('Scraping page ' + str(page) + ' of ' + suburb + ' at ' + str(datetime.datetime.now()))

        # Get URL source HTML
        source_html = browser.scrape(url)

        # Parse data
        parser = html_parser.HTMLParser(source_html)
        property_df, secondary_df = parser.parse_data(data_type)
        time.sleep(1)

        # Cache results
        property_cache.append(property_df)
        secondary_cache.append(secondary_df)

        # Cache log data
        cache_data = {'URL': suburb_url,
                      'Suburb': suburb,
                      'Page': page,
                      'Timestamp': datetime.datetime.now()}
        if not property_df.empty or not secondary_df.empty:
            cache_data['Status'] = 'Successful'
            print('Page ' + str(page) + ' of ' + suburb + '... SUCCESS')
        else:
            cache_data['Status'] = 'Failed'
            print('Page ' + str(page) + ' of ' + suburb + '... FAILED')
        log_cache.append(cache_data)

    # After scraping 50 pages of this suburb, close the browser
    browser.close()


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
    # Specify the data type we are collecting
    data_collected = 'sold'

    # Get list of sold suburb URLs
    url_list = url_generator.create_url_list(data_collected)

    # Filter out suburbs which were recently scraped based on log file
    # TODO could make this just gather all files in the log folder and build the tuple automatically
    url_list = url_generator.filter_list(url_list, ('2019-12-24-12PM.xlsx', '2019-12-24-3AM.xlsx'))

    print(str(len(url_list)) + ' suburbs to go')

    # Create session for SQLite database
    database_name = 'realestate_database.db'
    db = database_models.Database(database_name=database_name)

    # Dataframe to store log data in
    log_df = pandas.DataFrame(columns=['URL', 'Suburb', 'Page', 'Status', 'Timestamp'])

    # Initialise multiprocessing lock manager and lists to cache data
    with multiprocessing.Manager() as manager:
        log_scraped = manager.list()

        property_results = manager.list()
        secondary_results = manager.list()

        try:
            # Map list of URLs to max number of processes, execute build database
            # This will go through the list sequentially, rather than randomly
            with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
                pool.starmap(gather_data, zip(url_list, repeat(data_collected), repeat(property_results), repeat(secondary_results), repeat(log_scraped)))

        # If something fails, save the data we have
        finally:
            # Concatenate list of dfs into single df
            property_results_df = pandas.concat(property_results)
            secondary_results_df = pandas.concat(secondary_results)

            # Back up these dataframes to cache files, as long as they're not empty
            os.makedirs('Caches', exist_ok=True)
            property_path = os.path.join('Caches', str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")) + '_property.xlsx')
            secondary_path = os.path.join('Caches', str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")) + '_' + data_collected + '.xlsx')
            if not property_results_df.empty:
                property_results_df.to_excel(property_path, index=False)
            if not secondary_results_df.empty:
                secondary_results_df.to_excel(secondary_path, index=False)
            print('Caching data gathered for this run to spreadsheets')

            # Append dataframes to database
            print('Appending ' + str(len(secondary_results_df.index)) + ' rows of gathered data to database')
            build_database(db, property_results_df, secondary_results_df, data_collected)

            # Kill database session
            db.engine.dispose()

            # Make sure log file is still created if process fails
            log_scraped = list(log_scraped)
            log_df = pandas.DataFrame(log_scraped)
            os.makedirs('Logs', exist_ok=True)
            log_path = os.path.join('Logs', str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")) + '.xlsx')
            log_df.to_excel(log_path, index=False)
            print('Creating log file for this run')
