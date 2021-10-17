from sqlalchemy import MetaData, Table, Column, insert, delete, select
from sqlalchemy.dialects.mysql import CHAR, INTEGER, TEXT, LONGTEXT
from sqlalchemy.engine.cursor import CursorResult

from .database import Database
from ..utils.uuid import generate_uuid
from ..utils.verify import uuid_verify, uid_verify, param_length_verify

metadata = MetaData()

marks = Table(
    "marks",
    metadata,
    Column("MarkUUID", CHAR(32), nullable=False),
    Column("UserUUID", CHAR(32), nullable=False),
    Column("MarkUid", INTEGER, nullable=False),
    Column("MarkReason", TEXT, nullable=False),
    Column("MarkEvidence", LONGTEXT)
)

db = Database()


class Marks:
    @staticmethod
    async def add(userUUID, uid, reason, evidence=""):
        uuid_verify(userUUID)
        uid_verify(uid)
        param_length_verify(reason, 65535)
        if evidence:
            param_length_verify(evidence, 4294967295)
        await db.execute(insert(marks).
                         values(MarkUUID=generate_uuid(), UserUUID=userUUID, MarkUid=uid, MarkReason=reason,
                                MarkEvidence=evidence))

    @staticmethod
    async def remove(markUUID):
        uuid_verify(markUUID)
        await db.execute(delete(marks).
                         where(marks.c.MarkUUID == markUUID))

    @staticmethod
    async def get(markUUID):
        uuid_verify(markUUID)
        result: CursorResult = await db.execute(select(marks).
                                                where(marks.c.MarkUUID == markUUID))
        return result.one()

    @staticmethod
    async def get_all(userUUID):
        uuid_verify(userUUID)
        result: CursorResult = await db.execute(select(marks).
                                                where(marks.c.UserUUID == userUUID))
        return result.all()

    @staticmethod
    async def get_by_uid(userUUID, uid):
        uuid_verify(userUUID)
        uid_verify(uid)
        result: CursorResult = await db.execute(select(marks).
                                                where(marks.c.UserUUID == userUUID).
                                                where(marks.c.MarkUid == uid))
        return result.all()
