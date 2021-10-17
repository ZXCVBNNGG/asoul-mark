from sqlalchemy import MetaData, Table, Column, insert, delete, select
from sqlalchemy.dialects.mysql import CHAR

from .database import Database
from ..utils.verify import uuid_verify

metadata = MetaData()

subscriptions = Table(
    "subscriptions",
    metadata,
    Column("UserUUID", CHAR(32), nullable=False),
    Column("MarkListUUID", CHAR(32), nullable=False)
)

db = Database()


class Subscriptions:
    @staticmethod
    async def add(userUUID, markListUUID):
        uuid_verify(userUUID)
        uuid_verify(markListUUID)
        await db.execute(insert(subscriptions).
                         values(UserUUID=userUUID, MarkListUUID=markListUUID))

    @staticmethod
    async def remove(userUUID, markListUUID):
        uuid_verify(userUUID)
        uuid_verify(markListUUID)
        await db.execute(delete(subscriptions).
                         where(subscriptions.c.UserUUID == userUUID).
                         where(subscriptions.c.MarkListUUID == markListUUID))

    @staticmethod
    async def get(userUUID):
        uuid_verify(userUUID)
        result = await db.execute(select(subscriptions).
                                  where(subscriptions.c.UserUUID == userUUID))
        return result.all()
