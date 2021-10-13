from hashlib import md5

from .config import Config


def get_hashed_password(password: str):
    md5_obj = md5()
    text_with_salt = password + Config.salt
    md5_obj.update(text_with_salt.encode("utf8"))
    return md5_obj.hexdigest()
