from typing import Optional, List
from fastapi import APIRouter, Request, Header, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.config import Settings
from app.models.index import (
    TunnelCreate,
    TunnelRead,
)
from app.db_ops import TunnelOps

settings = Settings()
templates = Jinja2Templates(directory=settings.TEMPLATE_DIR)
db = TunnelOps()

home_router = APIRouter(
    tags=["home"],
    responses={404: {"description": "Home Not found"}},
)


@home_router.get("/", response_class=HTMLResponse)
async def home(request: Request, hx_request: Optional[str] = Header(None)):
    """
    Route for main home view.
    """
    context = {
        "request": request,
    }
    if hx_request:
        return templates.TemplateResponse("views/home-view.html", context)

    return templates.TemplateResponse("base.html", context)


@home_router.get("/settings", response_class=HTMLResponse)
async def app_settings(request: Request, hx_request: Optional[str] = Header(None)):
    """
    Route for App Settings.
    """
    context = {
        "request": request,
    }
    if hx_request:
        return templates.TemplateResponse("views/app-settings.html", context)

    return templates.TemplateResponse("base.html", context)


router = APIRouter(
    prefix="/tunnels",
    tags=["tunnels"],
    responses={404: {"description": "Tunnels Not found"}},
)


@router.get("/", response_class=HTMLResponse)
async def read_tunnels(request: Request, hx_request: Optional[str] = Header(None)):
    """
    Route to read all Tunnels in the database.
    """
    tunnels = await db.reads(TunnelRead)

    context = {
        "request": request,
        "tunnels": tunnels,
    }
    if hx_request:
        return templates.TemplateResponse("components/tunnel.html", context)

    return templates.TemplateResponse("base.html", context)


@router.get("/new", response_class=HTMLResponse)
async def new(request: Request):
    """
    Route to read all Tunnels in the database.
    """
    context = {
        "request": request,
    }

    return templates.TemplateResponse("views/tunnel-form.html", context)


@router.get("/{id}", response_class=HTMLResponse)
async def read_tunnel(request: Request, id: str):
    hx_request: Optional[str] = Header(None)
    """
    Route to read all blocks that belong to a Tunnel.
    """
    tunnel = await db.read(id)

    context = {
        "request": request,
        "tunnel": tunnel,
    }

    if hx_request:
        return templates.TemplateResponse("components/tunnel-open.html", context)

    return templates.TemplateResponse("base.html", context)


@router.post("/create")
async def create_tunnel(
    request: Request,
    name: str = Form(...),
    description: str = Form(...),
    hx_request: Optional[str] = Header(None),
):
    """
    Route to create a new Tunnel in the database.
    """
    db = TunnelOps()

    tunnels = await db.create(TunnelCreate(name=name, description=description))

    context = {
        "request": request,
        "tunnels": tunnels,
    }

    if hx_request:
        return templates.TemplateResponse("components/tunnel.html", context)

    return templates.TemplateResponse("base.html", context)


# @router.delete("/tunnels/delete")
# async def delete_tunnel(request: Request):
#     """
#     Route to delete a Tunnel in the database.
#     """
#     db = TunnelOps()

#     tunnels = await db.delete()

#     context = {
#         "request": request,
#         "tunnels": tunnels,
#     }

#     return templates.TemplateResponse("main.html", context)
