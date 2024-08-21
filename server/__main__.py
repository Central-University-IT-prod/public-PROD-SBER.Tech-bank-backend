from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from server.db.settings import init_db
from server.config import ALLOWED_ORIGINS, ADMIN_TOOLS_ON, DISABLE_DATABASE
from server.routers.meetings import meetings_router
from server.routers.representatives import representatives_router
from server.routers.admin import admin_router
from server.routers.operations import operations_router
from server.routers.clients import client_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # On startup:
    if not DISABLE_DATABASE:
        await init_db()
    yield
    # On shutdown:
    ...


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(representatives_router)
app.include_router(meetings_router)
app.include_router(operations_router)
app.include_router(client_router)

if ADMIN_TOOLS_ON:
    app.include_router(admin_router, prefix="/admin")


@app.get("/ping")
async def root():
    return {"message": "ok"}
