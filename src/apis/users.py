from fastapi import APIRouter
from pydantic import BaseModel

from ..databases import Users
from ..databases.users import user_verify_by_name, user_verify_by_uuid
from ..utils.exceptions import LoginFailedError
from ..utils.return_handler import return_handler

router = APIRouter()


class LoginBody(BaseModel):
    name: str
    password: str


class RegisterBody(BaseModel):
    name: str
    password: str


class ResetPasswordBody(BaseModel):
    name: str
    userUUID: str
    newPassword: str


@router.post("/user/login")
async def login(loginBody: LoginBody):
    await user_verify_by_name(loginBody.name, True)
    login_result = await Users.login(loginBody.name, loginBody.password)
    if not login_result:
        raise LoginFailedError
    data = {"name": login_result[0][1], "userUUID": login_result[0][0]}
    return return_handler(data)


@router.post("/user/register")
async def register(registerBody: RegisterBody):
    await user_verify_by_name(registerBody.name, False)
    await Users.register(registerBody.name, registerBody.password)
    return return_handler()


@router.post("/user/reset_password")
async def reset_password(resetPasswordBody: ResetPasswordBody):
    await user_verify_by_uuid(resetPasswordBody.userUUID, True)
    await Users.reset_password(resetPasswordBody.name, resetPasswordBody.userUUID, resetPasswordBody.newPassword)
    return return_handler()
