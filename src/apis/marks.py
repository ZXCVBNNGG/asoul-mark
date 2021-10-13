from typing import Optional

from fastapi import APIRouter, Cookie, Header
from pydantic import BaseModel

from ..databases import Marks
from ..utils.exceptions import NoPermissionError, NotFoundError
from ..utils.return_handler import return_handler
from ..utils.verify import userUUID_get

router = APIRouter()


class MarkAddBody(BaseModel):
    uid: int
    reason: str
    evidence: str = ""


class MarkRemoveBody(BaseModel):
    markUUID: str


def mark_verify(mark):
    if not mark:
        raise NotFoundError


def permission_verify(mark, userUUID):
    if not mark[1] == userUUID:
        raise NoPermissionError


@router.post("/mark/add")
async def add(markAddBody: MarkAddBody, UserUUID_C: Optional[str] = Cookie(None),
              UserUUID_H: Optional[str] = Header(None)):
    userUUID = userUUID_get(UserUUID_C, UserUUID_H)
    Marks.add(userUUID, markAddBody.uid, markAddBody.reason, markAddBody.evidence)
    return return_handler()


@router.post("/mark/remove")
async def remove(markRemoveBody: MarkRemoveBody, UserUUID_C: Optional[str] = Cookie(None),
                 UserUUID_H: Optional[str] = Header(None)):
    userUUID = userUUID_get(UserUUID_C, UserUUID_H)
    mark = Marks.get(markRemoveBody.markUUID)
    mark_verify(mark)
    permission_verify(mark, userUUID)
    Marks.remove(markRemoveBody.markUUID)
    return return_handler()


@router.get("/mark/get")
async def get(markUUID: str):
    mark = Marks.get(markUUID)
    mark_verify(mark)
    return return_handler({"markUUID": mark[0], "uid": mark[2], "reason": mark[3], "evidence": mark[4]})
