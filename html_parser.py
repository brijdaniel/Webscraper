"""
Parse scraped html and extract certain data, depending on what the source html was.
"""

import re
from datetime import datetime
from bs4 import BeautifulSoup
import pandas
import numpy


class HTMLParser:
    """
    Class to create HTML parser, which has methods to parse different types of data (e.g. sold, current listings etc),
    but always automatically extracts data to populate the 'Property' table in the SQLite database.
    """

    def __init__(self, html):
        """
        :param html: Source HTML from realestate.com.au
        """

        # Load html content
        self.soup = BeautifulSoup(html, 'html.parser')

    def parse_data(self, *args):
        """
        Main method (static) of HTMLParser object. Parses input HTML, extracts property data and then extracts specific data
        depending on HTML source. Arguments (*args) are used to specify what source the data is from, and
        therefore call the appropriate parsing methods. Accepted args are: sold, rent, listed.

        :param self: Gives access to the HTML soup
        :param args: String specifying HTML data source and which parser to use
        :return: Two pandas dataframes, first being the Property data table, second being the specific source data table
        """

        # Create dataframes to store parsed data TODO this should be contained in the parse_propery etc methods somehow
        property_columns = ['Address', 'Suburb', 'Land_Size', 'Bedrooms', 'Bathrooms', 'Car_Spaces', 'Property_Type']
        sold_columns = ['Price', 'Date_Sold', 'Address']
        property_df = pandas.DataFrame(columns=property_columns)
        sold_df = pandas.DataFrame(columns=sold_columns)

        # Locate each property in results, loop through to extract data
        for self.property_data in self.soup.findAll('article', attrs={"data-testid": "ResidentialCard"}):
            property_data = self.__parse_property(self.property_data)
            property_df = property_df.append(property_data, ignore_index=True)

            if 'sold' in args:
                sold_data = self.__parse_sold(self.property_data)
                # Make sure data returned is valid, otherwise skip this entry to df
                if sold_data:
                    sold_data['Address'] = property_data['Address']  # link the address so the foreign key value can populate
                    sold_df = sold_df.append(sold_data, ignore_index=True)

            # TODO add functionality for other *args

        return property_df, sold_df

    @staticmethod
    def __parse_property(property_data):
        """
        Private static method to extract property data from soup contents. Returns data in a dict ready to be appended to a dataframe.

        :param property_data: Data returned from loop through HTML soup
        :return: Dict of extracted data
        """

        # Find address and suburb. Note suburb is left in the address string too to ensure addresses are unique,
        # and can therefore be used as the primary key for each table in the database
        # .contents extracts the price as a list of length 1, so [0] accesses the actual value
        address = str(property_data.find('span', attrs={'class': ''}).contents[0])
        suburb = address.split(', ')[-1]

        # Find land size, bedrooms, bathrooms, car spaces and property type if given
        try:
            # Convert from 'bs4.element.NavigableString' to int, removing commas in str
            land_size = property_data.find('span', attrs={'class': re.compile('property-size__icon property-size.*')}).contents[0]
            land_size = int(land_size.replace(',', ''))
        except (AttributeError, ValueError, TypeError):
            land_size = numpy.NaN
        try:
            bedrooms = int(property_data.find('span', attrs={
                'class': 'general-features__icon general-features__beds'}).contents[0])
        except (AttributeError, ValueError, TypeError):
            bedrooms = numpy.NaN
        try:
            bathrooms = int(property_data.find('span', attrs={
                'class': 'general-features__icon general-features__baths'}).contents[0])
        except (AttributeError, ValueError, TypeError):
            bathrooms = numpy.NaN
        try:
            car_spaces = int(property_data.find('span', attrs={
                'class': 'general-features__icon general-features__cars'}).contents[0])
        except (AttributeError, ValueError, TypeError):
            car_spaces = numpy.NaN
        try:
            property_type = str(property_data.find('span', attrs={'class': 'residential-card__property-type'}).contents[0])
        except (AttributeError, ValueError, TypeError):
            property_type = numpy.NaN

        # Put this data into a row of the df
        data = {'Address': address,
                'Suburb': suburb,
                'Land_Size': land_size,
                'Bedrooms': bedrooms,
                'Bathrooms': bathrooms,
                'Car_Spaces': car_spaces,
                'Property_Type': property_type}

        return data

    @staticmethod
    def __parse_sold(property_data):
        """
        Private static method to extract sold data from soup contents. Returns data in a dict ready to be appended to a dataframe.

        :param property_data: Data returned from loop through HTML soup
        :return: Dict of extracted data
        """

        # Find property price by searching for <span class='property-price'>$xxx,xxx</span>
        # then convert this price string into an int, removing the $ and , chars
        price = property_data.find('span', attrs={'class': 'property-price'}).contents[0]
        try:
            price = int(re.sub(r'[^\d.]', '', price))
            # If sold price is given as a range, eg '$1,250,000 - $1,500,000' then above expression will return
            # '12500001500000', so assert we are getting reaslistic data, otherwise discard
            assert 100000 < price < 9999999
        # If something is wrong with the price data then we discard this property
        except (AttributeError, ValueError, TypeError, AssertionError):
            return None

        # Find date sold - since this span that contains the date sold has no class or other attribute to filter it by,
        # we must get all spans, then search through them individually for the phrase 'Sold on'
        # Then split the string at 'Sold on ' and '<date>' to extract just the date
        date_sold = numpy.NaN
        spans = property_data.find_all('span')
        span_contents = [span.get_text() for span in spans]
        for span in span_contents:
            if re.search('^Sold on ', span):
                date_sold = re.split('^Sold on ', span)[1]
                break
        # Process this date string into proper datetime object
        try:
            date_sold = datetime.strptime(date_sold, '%d %b %Y').date()
        # As with price, if something is wrong with the date data then we discard this property
        except (AttributeError, ValueError, TypeError):
            return None

        # Put this data into a row of the df
        data = {'Price': price, 'Date_Sold': date_sold}

        return data


if __name__ == '__main__':
    web_page = './page2.html'
    # results = parse_sold(web_page)
    # print(results)
