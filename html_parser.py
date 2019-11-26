"""
Parse scraped html and extract certain data, depending on what the source html was.
"""

import re
from datetime import datetime
from bs4 import BeautifulSoup
import pandas
import numpy


def parse_sold(html):
    """
    Parses html of Sold properties and extracts Address, Price, Date Sold, Land Size, Bedrooms, Bathrooms, Car Spaces
    and Property Type. Returns this data in a pandas dataframe with those column headings.

    :param html: Source HTML from https://www.realestate.com.au/sold/in-sa/list-1 or similar search
    :return: Pandas dataframe of results
    """

    # Load html content
    content = BeautifulSoup(open(html), 'html.parser')

    # Create dataframe to store scraped data
    column_labels = ['Address', 'Suburb', 'Price', 'Date_Sold', 'Land_Size', 'Bedrooms', 'Bathrooms', 'Car_Spaces', 'Property_Type']
    df = pandas.DataFrame(columns=column_labels)

    # Locate each property in results, loop through to extract data
    for residential_property in content.findAll('article', attrs={"data-testid": "ResidentialCard"}):
        # Find address and suburb. Note suburb is left in the address string too to ensure addresses are unique,
        # and can therefore be used as the primary key for each table in the database
        # .contents extracts the price as a list of length 1, so [0] accesses the actual value
        address = residential_property.find('span', attrs={'class': ''}).contents[0]
        suburb = address.split(', ')[1]

        # Find property price by searching for <span class='property-price'>$xxx,xxx</span>
        # then convert this price string into an in, removing the $ and , chars
        price = residential_property.find('span', attrs={'class': 'property-price'}).contents[0]
        price = int(re.sub(r'[^\d.]', '', price))

        # Find date sold - since this span that contains the date sold has no class or other attribute to filter it by,
        # we must get all spans, then search through them individually for the phrase 'Sold on'
        # Then split the string at 'Sold on ' and '<date>' to extract just the date
        date_sold = numpy.NaN
        spans = residential_property.find_all('span')
        span_contents = [span.get_text() for span in spans]
        for span in span_contents:
            if re.search('^Sold on ', span):
                date_sold = re.split('^Sold on ', span)[1]
                break
        # Process this date string into proper datetime object
        date_sold = datetime.strptime(date_sold, '%d %b %Y').date()

        # Find land size, bedrooms, bathrooms, car spaces and property type if given
        try:
            # Convert from 'bs4.element.NavigableString' to int
            land_size = int(residential_property.find('span', attrs={'class': 'property-size__icon property-size__building'}).contents[0])
        except AttributeError:
            land_size = numpy.NaN
        try:
            bedrooms = int(residential_property.find('span', attrs={'class': 'general-features__icon general-features__beds'}).contents[0])
        except AttributeError:
            bedrooms = numpy.NaN
        try:
            bathrooms = int(residential_property.find('span', attrs={'class': 'general-features__icon general-features__baths'}).contents[0])
        except AttributeError:
            bathrooms = numpy.NaN
        try:
            car_spaces = int(residential_property.find('span', attrs={'class': 'general-features__icon general-features__cars'}).contents[0])
        except AttributeError:
            car_spaces = numpy.NaN
        try:
            property_type = residential_property.find('span', attrs={'class': 'residential-card__property-type'}).contents[0]
        except AttributeError:
            property_type = numpy.NaN

        # Put this data into a row of the df
        data = {'Address': address,
                'Suburb': suburb,
                'Price': price,
                'Date_Sold': date_sold,
                'Land_Size': land_size,
                'Bedrooms': bedrooms,
                'Bathrooms': bathrooms,
                'Car_Spaces': car_spaces,
                'Property_Type': property_type}

        df = df.append(data, ignore_index=True)

    return df


if __name__ == '__main__':
    web_page = './page2.html'
    results = parse_sold(web_page)
    print(results)
