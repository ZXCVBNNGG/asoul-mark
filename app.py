import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.apis import users, marks, mark_lists, subscribe
from src.utils.exceptions import BaseError
from src.utils.return_handler import return_handler

app = FastAPI(openapi_url="")
app.include_router(users.router)
app.include_router(marks.router)
app.include_router(mark_lists.router)
app.include_router(subscribe.router)


@app.exception_handler(BaseError)
async def exception_handler(request: Request, exc: BaseError):
    return JSONResponse(
        status_code=exc.code,
        content={"code": exc.code, "msg": exc.message},
    )


@app.get("/")
async def root():
    return return_handler()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
