"""
Main interface for executing webscraper

Currently only works with html downloaded and stored locally in the project root directory, as the scraping side doesn't yet work.
"""

from sqlalchemy.exc import IntegrityError
import html_parser, database_models

# Specify path to source html
source_html = './page2.html'  # local html source in root directory

# Get data from html
sold_properties_df = html_parser.parse_sold(source_html)

# Create engine for SQLite database
engine = database_models.db.create_engine('sqlite:///realestate_database.db')

# Add dataframe to database - below line fails when duplicate entries occur, hence iterate through df manually which is slow...
# sold_properties_df.to_sql('Sold Property', con=engine, if_exists='append', index=False)
for i in range(len(sold_properties_df)):
    try:
        sold_properties_df.iloc[i:i+1].to_sql(name='Sold Property', if_exists='append', con=engine, index=False)
    except IntegrityError:
        pass
