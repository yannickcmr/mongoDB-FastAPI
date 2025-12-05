""" File for establishing DB connection """

import os
from dotenv import load_dotenv
import pymongo


""" Connection Function """

def db_connect(name: str) -> pymongo.MongoClient:
    """ Function to establish a connection.

    Returns:
        pymongo.MongoClient: MongoClient or None.
    """
    print("==> Start connecting to DB.")
    
    # loading .env file variables.
    try:
        load_dotenv()
        db_host = os.environ.get("DB_HOST", default="localhost:27017")
        db_name = os.environ.get("DB_NAME", default="Database")
        db_user = os.environ.get("DB_USER", default="admin")
        db_password = os.environ.get("DB_PASSWORD", default="password")

        print(f"==> Gathered DB .env: {db_host} - {db_name} - {db_user}")

    except Exception as e:
        raise ImportWarning(f"==> Could not gather environment variables: {e}")

    # connecting to database.
    try:
        session = pymongo.MongoClient(
            host=db_host,
            username=db_user,
            password=db_password,
            authSource="admin",
            timeoutMS=1000
        )
        collection = session[db_name][name]
        print(f"==> Connected to Collection: {collection}")

        if collection is None:
            raise ConnectionError(f"Could not connect to Collection: {name}")

    except Exception as e:
        raise ConnectionError(f"==> Could not connect to DB: {e}")

    return collection
