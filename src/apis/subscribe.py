from fastapi import APIRouter, Request
from pydantic import BaseModel

from ..databases import Subscriptions
from ..databases.users import user_verify_by_uuid
from ..utils.return_handler import return_handler
from ..utils.verify import userUUID_get

router = APIRouter()


class SubscribeBody(BaseModel):
    markListUUID: str


@router.post("/subscribe/add")
async def subscribe_add(subscribeBody: SubscribeBody, request: Request):
    userUUID = userUUID_get(request)
    user_verify_by_uuid(userUUID, True)
    Subscriptions.add(userUUID, subscribeBody.markListUUID)
    return return_handler()


@router.post("/subscribe/remove")
async def subscribe_remove(subscribeBody: SubscribeBody, request: Request):
    userUUID = userUUID_get(request)
    user_verify_by_uuid(userUUID, True)
    Subscriptions.remove(userUUID, subscribeBody.markListUUID)
    return return_handler()


@router.get("/subscribe/get")
async def subscribe_get(request: Request):
    userUUID = userUUID_get(request)
    user_verify_by_uuid(userUUID, True)
    subscriptions = Subscriptions.get(userUUID)
    return return_handler([i[1] for i in subscriptions])
