"""
Main interface for executing webscraper and building SQLite database.
"""
import datetime
from sqlalchemy.exc import IntegrityError
import html_parser, database_models, scraper, url_generator

if __name__ == '__main__':
    # Get list of sold suburb URLs
    url_list = url_generator.create_url_list('sold')

    # Iterate through list, searching one suburb at time
    for suburb_url in url_list:
        # Unpack suburb from URL for debugging, probably a nicer way to do this
        suburb = (suburb_url.split('in-')[1]).split(',')[0]

        # Iterate through 50 pages of search results (can't seem to get more than 50)
        for page in range(1, 50+1):
            # Flag for checking if the data in the current suburb is still valid (ie new data)
            break_flag = False

            # URL to scrape
            url = suburb_url + str(page)

            print('Scraping page ' + str(page) + ' of ' + suburb + ' at ' + str(datetime.datetime.now()))

            # Get URL source HTML
            source_html = scraper.scrape(url)

            # Parse data
            parser = html_parser.HTMLParser(source_html)
            property_df, sold_df = parser.parse_data('sold')

            # Create engine for SQLite database
            database_name = 'realestate_database.db'
            db = database_models.Database(database_name=database_name)

            # Add dataframe to database
            # TODO below line fails when duplicate entries occur, hence iterate through df
            #  manually which is slow...
            #  sold_properties_df.to_sql('Sold Property', con=engine, if_exists='append', index=False)
            #  Optimise below code later on
            for i in range(len(property_df)):
                try:
                    property_df.iloc[i:i+1].to_sql(name='Property', if_exists='append', con=db.engine, index=False)
                except IntegrityError:
                    pass

            if not sold_df.empty:
                for x in range(len(sold_df)):
                    try:
                        sold_df.iloc[x:x+1].to_sql(name='Sold History', if_exists='append', con=db.engine, index=False)
                    except IntegrityError:
                        # Set flag to show that the end of valid results in this suburb has been reached
                        break_flag = True

            # Break from this suburb if we start to encounter results that are already in the db
            # TODO note this is only valid if the entire suburbs data has been fully scraped at least once
            if break_flag:
                break_flag = False
                # break TODO uncomment this once full database baseline has been scraped
