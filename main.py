import uvicorn
from fastapi import FastAPI, APIRouter
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from repositories.async_db import AsyncDB
from routers.v1 import example_router
import settings


@asynccontextmanager
async def lifespan():
    await AsyncDB.warm_up()
    yield

def register_middleware(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ORIGINS,
        allow_credentials=True,
        allow_methods=settings.METHODS,
        allow_headers=settings.HEADERS,
    )

def register_routes(app: FastAPI) -> None:
    prefix_version = "/v1"
    app.include_router(router=example_router.router, prefix=f"{prefix_version}")

def create_app() -> FastAPI:
    app = FastAPI(
        title="Example APP",
        version=settings.VERSION,
        lifespan=lifespan,
        docs_url="/docs",
    )
    register_middleware(app)
    register_routes(app)

    return app

def run() -> None:
    try:
        import uvloop
        uvloop.install()
    except ImportError:
        print("uvloop not found, using standard asyncio loop.")

    if settings.ENV == "dev":
        uvicorn.run(
            "main:app",
            host=settings.HOST,
            port=settings.PORT,
            log_level="error",
            ws_ping_interval=10,
            loop="auto",
            reload=True,
        )
    else:
        uvicorn.run(
            create_app(),
            host=settings.HOST,
            port=settings.PORT,
            log_level="error",
            ws_ping_interval=10,
            loop="auto",
        )

app = create_app()

if __name__ == "__main__":
    # gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:9000 app_loader:app
    run()
