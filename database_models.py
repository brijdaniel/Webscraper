"""
Define classes used for SQLite database construction.
"""

import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base

# Create Base object to inherit from for all defined database models
Base = declarative_base()


class __Property:
    """
    Abstract base class for representing a property. Defines common attributes used in the database.
    """

    address = db.Column(db.String, primary_key=True)
    suburb = db.Column(db.String)
    land_size = db.Column(db.Integer)
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    car_spaces = db.Column(db.Integer)
    property_type = db.Column(db.String)


class SoldProperty(Base, __Property):
    """
    Class representing a Sold Property in the database. Inherits from SQLAlchemy Base and abstract class __Property
    """

    __tablename__ = 'Sold Property'

    price = db.Column(db.Integer)
    date_sold = db.Column(db.Date)

    def __repr__(self):
        return '<Sold Property (address={}, suburb={}, price={}, date sold={}, land size={}, bedrooms={}, bathrooms={}, car spaces={}, property type={}>'.format(
            self.address, self.suburb, self.price, self.date_sold, self.land_size, self.bedrooms, self.bathrooms, self.car_spaces, self.property_type)
