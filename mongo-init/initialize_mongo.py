import time
import os
import pymongo

def init_mongo_db():
    MONGO_URL = os.getenv("MONGODB_URL", "mongodb://admin:password@mongodb:27017/Database")
    DB_NAME = os.getenv("MONGO_DB_NAME", "Database")
    
    for i in range(5):
        try:
            client = pymongo.MongoClient(MONGO_URL)
            db = client[DB_NAME]

            print(f"Connection attempt {i+1}: Success.")

            # Insert data from your init-mongo.js logic
            db.create_collection("Users")
            db.Users.create_index([("userID", pymongo.ASCENDING)], unique=True)
            
            users_data = [
              {"userID": 1, "name": "Alice", "email": "alice_kitzler@gmx.de"},
              {"userID": 2, "name": "Pablo", "email": "pablo.mendez@gmail.com"},
              {"userID": 3, "name": "Jänsen", "email": "jaensen-freidrich-heinrichson@gmail.com"}
            ]
            db.Users.insert_many(users_data)
            
            print("Database initialized successfully.")
            client.close()
            return

        except pymongo.errors.ConnectionFailure as e:
            print(f"Connection attempt {i+1}: Failed. Retrying in 5 seconds... Error: {e}")
            time.sleep(5)
        except pymongo.errors.CollectionInvalid as e:
            print("Collection already exists, skipping creation.")
            return
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return


if __name__ == "__main__":
    init_mongo_db()
