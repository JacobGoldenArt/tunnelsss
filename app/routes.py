from fastapi import APIRouter, Request
from jinja2_fragments.fastapi import Jinja2Blocks
from app.models.index import (
    TunnelCreate,
    TunnelRead,
    BlockCreate,
    BlockRead,
)
from app.db_ops import TunnelOps, BlockOps

from app.config import Settings

settings = Settings()
templates = Jinja2Blocks(directory=settings.TEMPLATE_DIR)
router = APIRouter()


@router.post("/tunnels/create")
async def create_tunnel(request: Request, create: TunnelCreate):
    """
    Route to create a new Tunnel in the database.
    """
    db = TunnelOps()

    tunnels = await db.create(create)

    context = {
        "request": request,
        "tunnels": tunnels,
    }

    return templates.TemplateResponse("main.html", context)


@router.get("/tunnels")
async def read_tunnel(request: Request):
    """
    Route to read a Tunnel in the database.
    """
    db = TunnelOps()

    tunnels = await db.read(TunnelRead)

    context = {
        "request": request,
        "tunnels": tunnels,
    }

    if not context["tunnels"]:
        context["tunnels"] = "No Tunnels Found"

    return templates.TemplateResponse("main.html", context)


@router.delete("/tunnels/delete")
async def delete_tunnel(request: Request):
    """
    Route to delete a Tunnel in the database.
    """
    db = TunnelOps()

    tunnels = await db.delete()

    context = {
        "request": request,
        "tunnels": tunnels,
    }

    return templates.TemplateResponse("main.html", context)


@router.post("/blocks/create")
async def create_block(request: Request, create: BlockCreate):
    """
    Route to create a new Block in the database.
    """
    db = BlockOps()

    blocks = await db.create(create)

    context = {
        "request": request,
        "blocks": blocks,
    }

    return templates.TemplateResponse("main.html", context)


@router.get("/blocks/read")
async def read_blocks(request: Request):
    """
    Route to read all Blocks in the database.
    """
    db = BlockOps()

    blocks = await db.reads(BlockRead)

    context = {
        "request": request,
        "blocks": blocks,
    }

    if not context["blocks"]:
        context["blocks"] = "No Blocks Found"

    return templates.TemplateResponse("main.html", context)


@router.get("/block/read/{id}")
async def read_block(request: Request, id: str):
    """
    Route to read a Block by id in the database.
    """
    db = BlockOps()

    blocks = await db.read(id)

    context = {
        "request": request,
        "blocks": blocks,
    }

    return templates.TemplateResponse("main.html", context)


@router.delete("/blocks/delete")
async def delete_blocks(request: Request):
    """
    Route to delete a All Blocks in the database.
    """
    db = BlockOps()

    blocks = await db.deletes()

    context = {
        "request": request,
        "blocks": blocks,
    }

    return templates.TemplateResponse("main.html", context)


@router.delete("/blocks/delete/{id}")
async def delete_block(request: Request, id: str):
    """
    Route to delete a Block by ID in the database.
    """
    db = BlockOps()

    blocks = await db.delete(id)

    context = {
        "request": request,
        "blocks": blocks,
    }

    return templates.TemplateResponse("main.html", context)
