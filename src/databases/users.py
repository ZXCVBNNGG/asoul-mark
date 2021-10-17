from sqlalchemy import MetaData, Table, Column, insert, select, update
from sqlalchemy.dialects.mysql import CHAR, VARCHAR

from .database import Database
from ..utils.exceptions import UserAlreadyExistError, UserNotExistError
from ..utils.md5 import get_hashed_password
from ..utils.uuid import generate_uuid
from ..utils.verify import param_length_verify, uuid_verify

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("UserUUID", CHAR(32), nullable=False),
    Column("Name", VARCHAR(128), nullable=False),
    Column("PasswordMD5", VARCHAR(64), nullable=False)
)

db = Database()


class Users:
    @staticmethod
    async def register(name, password):
        param_length_verify(name, 128)
        param_length_verify(get_hashed_password(password), 64)
        await db.execute(insert(users).
                         values(UserUUID=generate_uuid(), Name=name, PasswordMD5=get_hashed_password(password)))

    @staticmethod
    async def login(name, password):
        param_length_verify(name, 128)
        param_length_verify(get_hashed_password(password), 64)
        result = await db.execute(select(users).
                                  where(users.c.Name == name).
                                  where(users.c.PasswordMD5 == get_hashed_password(password)))
        return result.all()

    @staticmethod
    async def reset_password(name, userUUID, newPassword):
        param_length_verify(name, 128)
        uuid_verify(userUUID)
        param_length_verify(get_hashed_password(newPassword), 64)
        await db.execute(update(users).
                         where(users.c.Name == name).
                         where(users.c.UserUUID == userUUID).
                         values(PasswordMD5=get_hashed_password(newPassword)))

    @staticmethod
    async def exist_by_name(name):
        param_length_verify(name, 128)
        result = await db.execute(select(users).
                                  where(users.c.Name == name))
        if not result.all():
            return False
        return True

    @staticmethod
    async def exist_by_uuid(userUUID):
        uuid_verify(userUUID)
        result = await db.execute(select(users).
                                  where(users.c.UserUUID == userUUID))
        if not result.all():
            return False
        return True


# 被迫放在这
async def user_verify_by_name(name, has: bool):
    param_length_verify(name, 128)
    if not has:
        if await Users.exist_by_name(name):
            raise UserAlreadyExistError
    else:
        if not await Users.exist_by_name(name):
            raise UserNotExistError


async def user_verify_by_uuid(userUUID, has: bool):
    uuid_verify(userUUID)
    if not has:
        if await Users.exist_by_uuid(userUUID):
            raise UserAlreadyExistError
    else:
        if not await Users.exist_by_uuid(userUUID):
            raise UserNotExistError
