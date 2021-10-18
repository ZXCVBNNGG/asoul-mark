from sqlalchemy import MetaData, Table, Column, insert, delete, select
from sqlalchemy.dialects.mysql import CHAR, VARCHAR, TEXT, BOOLEAN
from sqlalchemy.engine.cursor import CursorResult

from .database import Database
from .marks import marks
from ..utils.uuid import generate_uuid
from ..utils.verify import uuid_verify, param_length_verify, param_type_verify, uid_verify

metadata = MetaData()

markLists = Table(
    "markLists",
    metadata,
    Column("MarkListUUID", CHAR(32), nullable=False),
    Column("MarkUUID", CHAR(32), nullable=False)
)

markListInfo = Table(
    "markListInfo",
    metadata,
    Column("MarkListUUID", CHAR(32), nullable=False),
    Column("UserUUID", CHAR(32), nullable=False),
    Column("Title", VARCHAR(128), nullable=False),
    Column("Description", TEXT),
    Column("Shared", BOOLEAN, nullable=False)
)

db = Database()


class MarkLists:
    @staticmethod
    async def create(userUUID: str, title: str, shared: bool, description: str = None):
        uuid_verify(userUUID)
        param_length_verify(title, 128)
        param_type_verify(shared, bool)
        if description:
            param_length_verify(description, 65535)
        await db.execute(insert(markListInfo).
                         values(MarkListUUID=generate_uuid(), UserUUID=userUUID, Title=title, Description=description,
                                Shared=shared))

    @staticmethod
    async def add_mark(markListUUID: str, markUUID: str):
        uuid_verify(markListUUID)
        uuid_verify(markUUID)
        await db.execute(insert(markLists).
                         values(MarkListUUID=markListUUID, MarkUUID=markUUID))

    @staticmethod
    async def remove_mark(markListUUID: str, markUUID: str):
        uuid_verify(markListUUID)
        uuid_verify(markUUID)
        await db.execute(delete(markLists).
                         where(markLists.c.MarkListUUID == markListUUID).
                         where(markLists.c.MarkUUID == markUUID))

    @staticmethod
    async def info(markListUUID: str):
        uuid_verify(markListUUID)
        result: CursorResult = await db.execute(select(markListInfo).
                                                where(markListInfo.c.MarkListUUID == markListUUID))
        return result.one()

    @staticmethod
    async def remove(markListUUID):
        uuid_verify(markListUUID)
        await db.execute(delete(markListInfo).
                         where(markListInfo.c.MarkListUUID == markListUUID))
        await db.execute(delete(markLists).
                         where(markLists.c.MarkListUUID == markListUUID))

    @staticmethod
    async def get_mark_lists(userUUID):
        uuid_verify(userUUID)
        result = await db.execute(select(markListInfo).
                                  where(markListInfo.c.UserUUID == userUUID))
        return result.all()

    @staticmethod
    async def get_marks(markListUUID):
        uuid_verify(markListUUID)
        result = await db.execute(select(marks).
                                  join(markLists, marks.c.MarkUUID == markLists.c.MarkUUID).
                                  where(markLists.c.MarkListUUID == markListUUID))
        return result.all()

    @staticmethod
    async def get_by_uid(markListUUID, markUid):
        uuid_verify(markListUUID)
        uid_verify(markUid)
        result = await db.execute(select(marks).
                                  join(markLists, marks.c.MarkUUID == markLists.c.MarkUUID).
                                  where(marks.c.MarkUid == markUid).
                                  where(markLists.c.MarkListUUID == markListUUID))
        return result.all()
