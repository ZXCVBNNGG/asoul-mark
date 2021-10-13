class BaseError(Exception):
    code: int
    message: str


class UnauthorizedError(BaseError):
    def __init__(self):
        self.code = 401
        self.message = "未经认证的操作"


class NotFoundError(BaseError):
    def __init__(self):
        self.code = 404
        self.message = "无请求内容"


class ParamTooLongError(BaseError):
    def __init__(self):
        self.code = 403
        self.message = "参数过长"


class ParamIsNoneError(BaseError):
    def __init__(self):
        self.code = 403
        self.message = "参数不可为空"


class UnCorrectUUIDError(BaseError):
    def __init__(self):
        self.code = 403
        self.message = "UUID格式不正确"


class UnCorrectUIDError(BaseError):
    def __init__(self):
        self.code = 403
        self.message = "UID格式不正确"


class UnCorrectParamError(BaseError):
    def __init__(self):
        self.code = 403
        self.message = "参数错误"


class LoginFailedError(BaseError):
    def __init__(self):
        self.code = 403
        self.message = "登录失败"


class UserAlreadyExistError(BaseError):
    def __init__(self):
        self.code = 403
        self.message = "已存在此用户"


class UserNotExistError(BaseError):
    def __init__(self):
        self.code = 403
        self.message = "此用户不存在"


class NoPermissionError(BaseError):
    def __init__(self):
        self.code = 403
        self.message = "无权执行此操作"
