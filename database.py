"""
Create and modify SQLite database. Only needs to be used in the first instance to create the database. Hence it is not
imported in main.py
"""
from sqlalchemy.orm import sessionmaker
import database_models


class Database:
    """
    Class for interacting with the SQLite database.

    :param database_name: Name of the database to create (str)
    """

    def __init__(self, database_name='realestate_database.db'):
        # Connect to database called 'realestate_database.db' located in current directory
        self.database_name = database_name
        self.engine = database_models.db.create_engine('sqlite:///' + self.database_name)
        # TODO need to find the source of Could not parse rfc1738 URL from string error

        # Map database models to database schema
        database_models.Base.metadata.create_all(self.engine)

        # Define session class for interacting with database
        Session = sessionmaker(bind=self.engine)

        # Create instance of Session object
        self.session = Session()
