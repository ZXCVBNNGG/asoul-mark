from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.apis import users, marks
from src.utils.exceptions import BaseError

app = FastAPI()
app.include_router(users.router)
app.include_router(marks.router)


@app.exception_handler(BaseError)
async def exception_handler(request: Request, exc: BaseError):
    return JSONResponse(
        status_code=exc.code,
        content={"code": exc.code, "msg": exc.message},
    )
