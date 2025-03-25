from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse

from src.api import router as api_router


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None]:
    yield


app = FastAPI(
    title="Salary project",
    version="1.0",
    lifespan=lifespan,
)

# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://dev.llhost.eu"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router)


@app.get("/", include_in_schema=False)
def root():
    return HTMLResponse(
        content='Welcome to Salary API! please visit <a href="/docs">docs</a>',
        status_code=status.HTTP_200_OK,
    )
