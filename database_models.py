"""
Define classes used for SQLite database construction.
"""

import sqlalchemy as db
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship


# Create SQL Base object to inherit from for all defined database models
Base = declarative_base()


class Database:
    """
    Class for interacting with the SQLite database.

    :param database_name: Name of the database to create (str)
    """

    def __init__(self, database_name='realestate_database.db'):
        # Connect to database called 'realestate_database.db' located in current directory
        self.database_name = database_name
        self.engine = db.create_engine('sqlite:///' + self.database_name)

        # Map database models to database schema
        Base.metadata.create_all(self.engine)

        # Define session class for interacting with database
        Session = sessionmaker(bind=self.engine)

        # Create instance of Session object
        self.session = Session()


class Property(Base):
    """
    Parent class for representing a property. Used for the core 'Property' table, which then links to
    sold history, rental history and current listings. This table is created from scraped data of Sold
    properties.
    """
    __tablename__ = 'Property'

    address = db.Column(db.String, primary_key=True)
    suburb = db.Column(db.String)
    land_size = db.Column(db.Integer)
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    car_spaces = db.Column(db.Integer)
    property_type = db.Column(db.String)

    # Foreign Key relationships
    sold_history = relationship('SoldHistory', order_by='SoldHistory.id', back_populates='property')
    rental_history = relationship('RentalHistory', order_by='RentalHistory.id', back_populates='property')
    current_listings = relationship('CurrentListings', order_by='CurrentListings.id', back_populates='property')

    def __repr__(self):
        """
        Modify the print output format to be more user friendly
        :return: str representing object data
        """
        return '<Sold Property (address={}, suburb={}, land size={}, bedrooms={}, bathrooms={}, car spaces={}, property type={}>'.format(
            self.address, self.suburb, self.land_size, self.bedrooms, self.bathrooms, self.car_spaces, self.property_type)


class SoldHistory(Base):
    """
    Class for defining the 'Sold History' table, which links the 'Property' table to previous sales data.
    The date_sold and address (which is a foreign key to the 'Property' table) act as a composite primary
    key for this table, ensuring that multiple entries of the same property sale do not exist by enforcing
    that each data entry is a unique combination of address and date_sold
    """
    # TODO need to implement rule that date_sold and address (from Property table) cannot duplicate

    __tablename__ = 'Sold History'

    date_sold = db.Column(db.Date, primary_key=True)
    price = db.Column(db.Integer)

    # Link Sold data to property table via address
    address = db.Column(db.String, ForeignKey('Property.address'), primary_key=True)
    property = relationship('Property', back_populates='sold_history')


class RentalHistory(Base):
    """
    Class for defining the 'Rental History' table, which links properties in the 'Property' table to previous
    rental data. Similar to the 'Sold History' table, this table's primary key is a composite of the date_rented
    and address (foreign key to 'Property' table) attributes.
    """

    __tablename__ = 'Rental History'

    date_rented = db.Column(db.Date, primary_key=True)
    price = db.Column(db.Integer)

    # Link Rental data to property table via address
    address = db.Column(db.String, ForeignKey('Property.address'), primary_key=True)
    property = relationship('Property', back_populates='rental_history')


class CurrentListings(Base):
    """
    Class for defining the current listings table, which links entries in the 'Property' table to their current
    asking price, if the property is on the market. This is the most dynamic table as listings are constantly
    changing. This table will need to be overwritten to ensure data is current. The address (foreign key to 'Property'
    table) is used as the primary key, as no property can be listed more than once.
    """
    # TODO will need a way to erase old listings from this table

    __tablename__ = 'Current Listings'

    asking_price = db.Column(db.Integer)

    # Link current listings to property table via address
    address = db.Column(db.String, ForeignKey('Property.address'), primary_key=True)
    property = relationship('Property', back_populates='current_listings')
