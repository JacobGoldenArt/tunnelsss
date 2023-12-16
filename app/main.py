from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import Settings
from app.routes import block_routes, tunnel_routes

settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Context manager for FastAPI app. It will run all code before `yield`
    on app startup, and will run code after `yeld` on app shutdown.
    """

    pass

    # try:
    #     subprocess.run(
    #         [
    #             "tailwindcss",
    #             "-i",
    #             str(settings.STATIC_DIR / "src" / "tw.css"),
    #             "-o",
    #             str(settings.STATIC_DIR / "css" / "main.css"),
    #         ]
    #     )
    # except Exception as e:
    #     print(f"Error running tailwindcss: {e}")

    # yield


def get_app() -> FastAPI:
    """Create a FastAPI app with the specified settings."""

    app = FastAPI(**settings.fastapi_kwargs)

    app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

    app.include_router(block_routes.router)
    app.include_router(tunnel_routes.home_router)
    app.include_router(tunnel_routes.router)

    return app


app = get_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8080,
        reload_includes=["*.css, *.html, *.py"],
        reload=True,
    )

    # reload: bool = False,
    # reload_dirs: typing.Optional[typing.Union[typing.List[str], str]] = None,
    # reload_includes: typing.Optional[typing.Union[typing.List[str], str]] = None,
    # reload_excludes: typing.Optional[typing.Union[typing.List[str], str]] = None,
