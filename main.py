"""
Main interface for executing webscraper and building SQLite database.

Currently only works with html downloaded and stored locally in the project root directory, as the scraping side doesn't yet work.
"""

from sqlalchemy.exc import IntegrityError
import html_parser, database_models

# Specify path to source html
source_html = './page2.html'  # local html source in root directory

# Parse data
parser = html_parser.HTMLParser(source_html)
property_df, sold_df = parser.parse_data('sold')

# Create engine for SQLite database
database_name = 'realestate_database.db'
engine = database_models.db.create_engine(database_name)

# Add dataframe to database - below line fails when duplicate entries occur, hence iterate through df manually which is slow...
# sold_properties_df.to_sql('Sold Property', con=engine, if_exists='append', index=False)
for i in range(len(property_df)):
    try:
        property_df.iloc[i:i+1].to_sql(name='Sold Property', if_exists='append', con=engine, index=False)
    except IntegrityError:
        pass

if sold_df:
    for i in range(len(sold_df)):
        try:
            sold_df.iloc[i:i+1].to_sql(name='Sold Property', if_exists='append', con=engine, index=False)
        except IntegrityError:
            pass
