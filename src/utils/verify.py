import regex

from .exceptions import ParamTooLongError, ParamIsNoneError, UnCorrectUUIDError, UnCorrectUIDError, UnCorrectParamError, \
    UnauthorizedError


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


def userUUID_get(UserUUID_C: str, UserUUID_H: str):
    if not UserUUID_H or not UserUUID_C:
        raise UnauthorizedError
    if UserUUID_C and UserUUID_H:
        return UserUUID_H
    else:
        if UserUUID_C:
            return UserUUID_C
        else:
            return UserUUID_H
