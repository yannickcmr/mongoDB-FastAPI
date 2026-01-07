""" Database API Endpoints for MongoDB operations """

from fastapi import APIRouter

from app.config.logging_config import create_logger
from app.validation.messages import MessageResponse, DataResponse, ErrorResponse
from app.validation.messages import DBGetUser, DBAddUser, DBDeleteUser
from app.model.database import DBUsers


""" Logging Function """

Logger = create_logger()
Logger.info("=> Logging initialized.")


""" API """

router = APIRouter(tags=['database'])

@router.get("/check_db", response_model=MessageResponse | ErrorResponse)
async def check_database(log_lvl: str = "info") -> MessageResponse | ErrorResponse:
    try:
        Logger.info(f"{DBUsers(log_lvl)=}")

        return {
            'msg': "/check_db success.",
            'code': 200,
            'data': None
        }

    except Exception as e:
        Logger.warning(f"Could not check DB: {e}")
        return ErrorResponse(msg="/check_db failed.")

@router.post("/get_user", response_model=DataResponse | ErrorResponse)
async def get_user(data: DBGetUser, log_lvl = "info") -> DataResponse | ErrorResponse:
    """ Endpoint for gathering User data from the DB.

    Args:
        data (DBGetUser): User Identifiers such as 'userID', 'email', etc.
        log_lvl (str, optional): Logger level. Defaults to "info".

    Returns:
        DataResponse: User Data from the DB.
    """
    Logger.setLevel(log_lvl.upper())
    Logger.debug(f"{data=}")

    try:
        response = DBUsers(log_lvl).get(data)
        if response['code'] != 200:
            Logger.warning(f"Could not add new User: {response['msg']}")

        user_data = response['data']
        Logger.debug(f"{user_data=}")

    except Exception as e:
        Logger.warning(f"Could not add body to User DB: {e}")
        return ErrorResponse(msg="Could not add body to User DB")

    return {
        "msg": "/add_user successful.",
        "code": 200,
        "data":  user_data
    }

@router.post("/add_user", response_model=DataResponse | ErrorResponse)
def add_user(data: DBAddUser, log_lvl = "info") -> DataResponse | ErrorResponse:
    """ Endpoint for adding a new User to the DB.

    Args:
        data (DBAddUser): User data including 'name', 'email', 'phone', etc.
        log_lvl (str, optional): Logger level. Defaults to "info".

    Returns:
        DataResponse: User Data.
    """
    Logger.setLevel(log_lvl.upper())
    Logger.debug(f"{data=}")

    try:
        response = DBUsers(log_lvl).add(data)
        if response['code'] != 200:
            Logger.warning(f"Could not add new User: {response['msg']}")

        user_data = response['data']
        Logger.debug(f"{user_data=}")

    except Exception as e:
        Logger.warning(f"Could not add body to User DB: {e}")
        return ErrorResponse(msg="Could not add body to User DB")

    return {
        "msg": "/add_user successful.",
        "code": 200,
        "data":  user_data
    }

@router.post("/delete_user", response_model=DataResponse | ErrorResponse)
def delete_user(data: DBDeleteUser, log_lvl = "info") -> DataResponse | ErrorResponse:
    """ Endpoint for deleting a User form the DB using 'userID', 'email', or 'phone'.

    Args:
        data (DBDeleteUser): User Identifiers such as 'userID', 'email', etc.
        log_lvl (str, optional): Logger level. Defaults to "info".

    Returns:
        DataResponse: User data removed from the DB.
    """
    Logger.setLevel(log_lvl.upper())
    Logger.debug(f"{data=}")

    try:
        response = DBUsers(log_lvl).delete(data)
        if response['code'] != 200:
            Logger.warning(f"Could not add new User: {response['msg']}")

        user_data = response['data']
        Logger.debug(f"{user_data=}")

    except Exception as e:
        Logger.warning(f"Could not add body to User DB: {e}")
        return ErrorResponse(msg="Could not add body to User DB")

    return {
        "msg": "/delete_user successful.",
        "code": 200,
        "data":  user_data
    }
