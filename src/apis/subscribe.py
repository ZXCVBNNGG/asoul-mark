from fastapi import APIRouter, Request
from pydantic import BaseModel

from ..databases import Subscriptions, MarkLists
from ..databases.users import user_verify_by_uuid
from ..utils.exceptions import NoPermissionError, CannotBeSelfError
from ..utils.return_handler import return_handler
from ..utils.verify import userUUID_get

router = APIRouter()


class SubscribeBody(BaseModel):
    markListUUID: str


@router.post("/subscribe/add")
async def subscribe_add(subscribeBody: SubscribeBody, request: Request):
    userUUID = userUUID_get(request)
    await user_verify_by_uuid(userUUID, True)
    info = await MarkLists.info(subscribeBody.markListUUID)
    if not info[4]:
        raise NoPermissionError
    if info[1] == userUUID:
        raise CannotBeSelfError
    await Subscriptions.add(userUUID, subscribeBody.markListUUID)
    return return_handler()


@router.post("/subscribe/remove")
async def subscribe_remove(subscribeBody: SubscribeBody, request: Request):
    userUUID = userUUID_get(request)
    await user_verify_by_uuid(userUUID, True)
    await Subscriptions.remove(userUUID, subscribeBody.markListUUID)
    return return_handler()


@router.get("/subscribe/get")
async def subscribe_get(request: Request):
    userUUID = userUUID_get(request)
    await user_verify_by_uuid(userUUID, True)
    subscriptions = await Subscriptions.get(userUUID)
    return return_handler([i[1] for i in subscriptions])
