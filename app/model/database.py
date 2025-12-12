""" Class for User Database Interaction """

from typing import Protocol, Optional
from random import randrange

from app.config.logging_config import create_logger
from app.config.db_connection_config import db_connect


""" Logging Function """

Logger = create_logger()
Logger.info("=> Logging initialized.")


""" Default Protocol """

class UserRequest(Protocol):
    """ Default User Request Class """
    userID: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    birthday: Optional[str] = None
    address: Optional[dict] = None
    ...

class UserResponse(Protocol):
    """ Default Response Class """
    msg: str
    code: int
    data: dict[str, dict]
    ...


""" User Database Model """

class DBUsers:
    def __init__(self, log_lvl: str = "info"):
        """ Method for initialization of the class """
        self._log_lvl = log_lvl.upper()

        try:
            self.db = db_connect('Users')
            if self.db is None:
                raise ConnectionError("Could not connect to User DB.")

            self.db.server_info()
        
        except Exception as e:
            raise ConnectionError(f"Could not initialize DB Connection: {e}")

    def get_id(self, new_id) -> UserResponse:
        """ Method for searching User by '_id' in mongoDB """
        Logger.setLevel(self._log_lvl)

        # searching for _id.
        try:
            data = self.db.find_one({"_id": new_id})
            if data is None:
                Logger.warning("Could not get User.")

            if '_id' in data:
                data.pop('_id')
            Logger.debug(f"{data=}")

        except Exception as e:
            Logger.warning(f"Could not find User: {e}")

        return {
            'msg': "get_id success.",
            'code': 200,
            'data': data
        }

    def get(self, data: UserRequest) -> UserResponse:
        """ Method to search User by 'userID', 'email' or 'phone' in mongoDB.  """
        Logger.setLevel(self._log_lvl)

        # generating query.
        try:
            if data.userID is not None:
                query = {"userID": data.userID}
            elif data.email is not None:
                query = {"email": data.email}
            elif data.phone is not None:
                query = {"phone": data.phone}
            else:
                raise ValueError("Could not find any identifier in data.")
        
        except Exception as e:
            Logger.warning(f"Cloud not create User query: {e}")

        try:
            data = self.db.find_one(query)
            if data is None:
                Logger.warning("Could not get User.")
            
            if '_id' in data:
                data.pop('_id')
            Logger.debug(f"{data=}")

        except Exception as e:
            Logger.warning(f"Cloud not create User body: {e}")
        
        return {
            'msg': "get success.",
            'code': 200,
            'data': data
        }

    def add(self, data: UserRequest) -> UserResponse:
        """ Method to add new User to mongoDB.  """
        Logger.setLevel(self._log_lvl)

        # creating body.
        try:
            user_body = {
                "userID": randrange(int(1e6), int(1e12)),
                "name": data.name,
                "email": data.email,
                "phone": data.phone,
                "birthday": data.birthday,
                "address": data.address
            }
            user_body = {k: v for k, v in user_body.items() if v is not None}
            Logger.debug(f"{user_body=}")

            if len(user_body) == 0:
                raise ValueError("Empty user Body.")

        except Exception as e:
            Logger.warning(f"Could not create User body: {e}")

        # adding to User database.
        try:
            response = self.db.insert_one(user_body)
            data = self.get_id(response.inserted_id)
            if data['code'] != 200:
                Logger.warning(f"Could not add User to DB: {data['msg']}")

            user = data['data']
            Logger.debug(f"{user=}")

        except Exception as e:
            Logger.warning(f"Could not add User to DB: {e}")

        return {
            "msg": "Success",
            "code": 200,
            "data": user
        }

    def delete(self, data: UserRequest) -> UserResponse:
        """ Method to delete User by 'userID', 'email' or 'phone' from mongoDB.  """
        Logger.setLevel(self._log_lvl)

        # deleting to User database.
        try:
            response = self.get(data)
            if response['code'] != 200:
                Logger.warning(f"Could not find User: {response['msg']}")
            
            user = response['data']
            Logger.debug(f"{user=}")

        except Exception as e:
            Logger.warning(f"Cloud not find User in DB: {e}")

        # generating query.
        try:
            if data.userID is not None:
                query = {"userID": data.userID}
            elif data.email is not None:
                query = {"email": data.email}
            elif data.phone is not None:
                query = {"phone": data.phone}
            else:
                raise ValueError("Could not find any identifier in data.")

            response = self.db.delete_one(query)
            Logger.debug(f"{response=}")

        except Exception as e:
            Logger.warning(f"Cloud not delete User from DB: {e}")
        
        return {
            "msg": "Success",
            "code": 200,
            "data": user
        }
