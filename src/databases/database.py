from sqlalchemy.ext.asyncio import create_async_engine

from ..utils.config import Config
from ..utils.singleton import Singleton


class Database(Singleton):
    def __init__(self):
        self.engine = create_async_engine(Config.url, echo=True, future=True, pool_pre_ping=True)

    async def execute(self, sql):
        async with self.engine.begin() as conn:
            result = await conn.execute(sql)
        return result
