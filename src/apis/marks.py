from fastapi import APIRouter, Request
from pydantic import BaseModel

from ..databases import Marks
from ..utils.return_handler import return_handler
from ..utils.verify import userUUID_get, mark_verify, permission_verify

router = APIRouter()


class MarkAddBody(BaseModel):
    uid: int
    reason: str
    evidence: str = ""


class MarkRemoveBody(BaseModel):
    markUUID: str


@router.post("/mark/add")
async def add(markAddBody: MarkAddBody, request: Request):
    userUUID = userUUID_get(request)
    Marks.add(userUUID, markAddBody.uid, markAddBody.reason, markAddBody.evidence)
    return return_handler()


@router.post("/mark/remove")
async def remove(markRemoveBody: MarkRemoveBody, request: Request):
    userUUID = userUUID_get(request)
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


@router.get("/mark/get_all")
async def get_all(request: Request):
    userUUID = userUUID_get(request)
    marks = Marks.get_all(userUUID)
    mark_verify(marks)
    return return_handler([{"markUUID": i[0], "uid": i[2], "reason": i[3], "evidence": i[4]} for i in marks])


@router.get("/mark/get_by_uid")
async def get_by_uid(uid: int, request: Request):
    userUUID = userUUID_get(request)
    marks = Marks.get_by_uid(userUUID, uid)
    mark_verify(marks)
    return return_handler([{"markUUID": i[0], "uid": i[2], "reason": i[3], "evidence": i[4]} for i in marks])
