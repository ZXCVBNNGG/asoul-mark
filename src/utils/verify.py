import regex
from fastapi import Request

from .exceptions import ParamTooLongError, ParamIsNoneError, UnCorrectUUIDError, UnCorrectUIDError, UnCorrectParamError, \
    UnauthorizedError, NotFoundError, NoPermissionError


def param_length_verify(param, max_length):
    if not bool(param):
        raise ParamIsNoneError
    if len(param.encode("utf8")) > max_length:
        raise ParamTooLongError


def uuid_verify(uuid):
    if not bool(uuid):
        raise ParamIsNoneError
    if not regex.match("[0-9a-fA-F]{32}", uuid):
        raise UnCorrectUUIDError


def uid_verify(uid):
    if not bool(uid):
        raise ParamIsNoneError
    if not type(uid) == int:
        raise UnCorrectUIDError
    if len(str(uid)) > 11:
        raise UnCorrectUIDError


def param_type_verify(param, type_):
    if type(param) != type_:
        raise UnCorrectParamError


def userUUID_get(request: Request):
    UserUUID_H = request.headers.get("UserUUID")
    UserUUID_C = request.cookies.get("UserUUID")
    if not UserUUID_H or UserUUID_C:
        raise UnauthorizedError
    if UserUUID_C and UserUUID_H:
        return UserUUID_H
    else:
        if UserUUID_C:
            return UserUUID_C
        else:
            return UserUUID_H


def mark_verify(mark):
    if not mark:
        raise NotFoundError


def mark_permission_verify(mark, userUUID):
    if not mark[1] == userUUID:
        raise NoPermissionError


def mark_list_permission_verify(markListInfo, userUUID):
    if not markListInfo[1] == userUUID:
        raise NoPermissionError
