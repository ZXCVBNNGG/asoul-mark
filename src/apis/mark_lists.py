from fastapi import APIRouter, Request
from pydantic import BaseModel

from ..databases import MarkLists
from ..databases.users import user_verify_by_uuid
from ..utils.return_handler import return_handler
from ..utils.verify import userUUID_get, mark_list_permission_verify

router = APIRouter()


class MarkListCreateBody(BaseModel):
    title: str
    description: str = ""
    shared: bool


class MarkListRemoveBody(BaseModel):
    markListUUID: str


class MarkListAddMarkBody(BaseModel):
    markListUUID: str
    markUUID: str


class MarkListRemoveMarkBody(BaseModel):
    markListUUID: str
    markUUID: str


class MarkListGetByUidBody(BaseModel):
    markListUUID: str
    uid: int


@router.post("/mark_list/create")
async def mark_list_create(markListBody: MarkListCreateBody, request: Request):
    userUUID = userUUID_get(request)
    await user_verify_by_uuid(userUUID, True)
    await MarkLists.create(userUUID, markListBody.title, markListBody.shared, markListBody.description)
    return return_handler()


@router.post("/mark_list/remove")
async def mark_list_remove(markListBody: MarkListRemoveBody, request: Request):
    userUUID = userUUID_get(request)
    await user_verify_by_uuid(userUUID, True)
    info = await MarkLists.info(markListBody.markListUUID)
    mark_list_permission_verify(info, userUUID)
    await MarkLists.remove(markListBody.markListUUID)
    return return_handler()


@router.get("/mark_list/info")
async def mark_list_info(markListUUID: str):
    info = await MarkLists.info(markListUUID)
    return return_handler({"markListUUID": info[0], "title": info[2], "description": info[3], "shared": info[4]})


@router.get("/mark_list/get")
async def mark_list_get(request: Request):
    userUUID = userUUID_get(request)
    await user_verify_by_uuid(userUUID, True)
    mark_lists = await MarkLists.get_mark_lists(userUUID)
    return return_handler(
        [{"markListUUID": info[0], "title": info[2], "description": info[3], "shared": info[4]} for info in mark_lists])


@router.get("/mark_list/get_marks")
async def mark_list_get_marks(markListUUID: str, request: Request):
    userUUID = userUUID_get(request)
    await user_verify_by_uuid(userUUID, True)
    info = await MarkLists.info(markListUUID)
    if not info[4]:
        mark_list_permission_verify(info, userUUID)
    marks = await MarkLists.get_marks(markListUUID)
    return return_handler([{"markUUID": i[0], "uid": i[2], "reason": i[3], "evidence": i[4]} for i in marks])


@router.post("/mark_list/add_mark")
async def mark_list_add_mark(markBody: MarkListAddMarkBody, request: Request):
    userUUID = userUUID_get(request)
    await user_verify_by_uuid(userUUID, True)
    info = await MarkLists.info(markBody.markListUUID)
    mark_list_permission_verify(info, userUUID)
    await MarkLists.add_mark(markBody.markListUUID, markBody.markUUID)
    return return_handler()


@router.post("/mark_list/remove_mark")
async def mark_list_remove_mark(markBody: MarkListRemoveMarkBody, request: Request):
    userUUID = userUUID_get(request)
    await user_verify_by_uuid(userUUID, True)
    info = await MarkLists.info(markBody.markListUUID)
    mark_list_permission_verify(info, userUUID)
    await MarkLists.remove_mark(markBody.markListUUID, markBody.markUUID)
    return return_handler()


@router.get("/mark_list/get_marks_by_uid")
async def mark_list_get_marks_by_uid(markListUUID: str, uid: int, request: Request):
    userUUID = userUUID_get(request)
    await user_verify_by_uuid(userUUID, True)
    info = await MarkLists.info(markListUUID)
    if not info[4]:
        mark_list_permission_verify(info, userUUID)
    marks = await MarkLists.get_by_uid(markListUUID, uid)
    return return_handler([{"markUUID": i[0], "uid": i[2], "reason": i[3], "evidence": i[4]} for i in marks])
