from sqlalchemy import create_engine

from ..utils.config import Config
from ..utils.singleton import Singleton


class Database(Singleton):
    def __init__(self):
        self.engine = create_engine(Config.url, echo=True, future=True, pool_pre_ping=True)

    def execute(self, sql):
        with self.engine.begin() as conn:
            result = conn.execute(sql)
        return result
