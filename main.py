"""
Main interface for executing webscraper and building SQLite database.
"""
import datetime
from sqlalchemy.exc import IntegrityError
import html_parser, database_models, scraper

if __name__ == '__main__':
    # Iterate through all 12,000 pages of sold results in SA
    for page in range(1, 12234+1):
        print('Scraping page ' + str(page) + ' of 12,234 at ' + str(datetime.datetime.now()))
        # URL to scrape
        url = 'https://www.realestate.com.au/sold/in-south+australia%3b/list-' + str(page)

        # Get URL source HTML
        source_html = scraper.scrape(url)

        # Parse data
        parser = html_parser.HTMLParser(source_html)
        property_df, sold_df = parser.parse_data('sold')

        # Create engine for SQLite database
        database_name = 'realestate_database.db'
        db = database_models.Database(database_name=database_name)

        # Add dataframe to database - below line fails when duplicate entries occur, hence iterate through df manually which is slow...
        # Optimise below code later on
        # sold_properties_df.to_sql('Sold Property', con=engine, if_exists='append', index=False)
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
                    pass
