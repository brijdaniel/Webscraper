"""
Create and modify SQLite database.
"""
from sqlalchemy.orm import sessionmaker
import database_models


class Database:
    """
    Class for interacting with the SQLite database.
    """

    def __init__(self):
        # Connect to database called 'realestate_database.db' located in current directory
        self.engine = database_models.db.create_engine('sqlite:///realestate_database.db')

        # Map database models to database schema
        database_models.Base.metadata.create_all(self.engine)

        # Define session class for interacting with database
        Session = sessionmaker(bind=self.engine)

        # Create instance of Session object
        self.session = Session()
