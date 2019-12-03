"""
Main interface for executing webscraper and building SQLite database.

Currently only works with html downloaded and stored locally in the project root directory, as the scraping side doesn't yet work.
"""

from sqlalchemy.exc import IntegrityError
import html_parser, database_models, scraper

# URL to scrape
url = 'https://www.realestate.com.au/sold/in-henley+beach/list-1'

# Get URL source HTML
soup = scraper.scrape(url)  # './page2.html'  # local html source in root directory

# Parse data
parser = html_parser.HTMLParser(soup)
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
    for i in range(len(sold_df)):
        try:
            sold_df.iloc[i:i+1].to_sql(name='Sold History', if_exists='append', con=db.engine, index=False)
        except IntegrityError:
            pass
