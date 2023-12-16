from typing import List, Optional
from fastapi import APIRouter, Request, Header, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.config import Settings
from app.models.index import (
    BlockCreate,
    BlockRead,
)
from app.db_ops import BlockOps


settings = Settings()
templates = Jinja2Templates(directory=settings.TEMPLATE_DIR)
db = BlockOps()

router = APIRouter(
    prefix="/blocks",
    tags=["blocks"],
    responses={404: {"description": "Blocks Not found"}},
)


@router.get("/", response_class=HTMLResponse)
async def read_blocks(request: Request, hx_request: Optional[str] = Header(None)):
    """
    Route to read all Blocks in the database.
    """
    blocks = await db.reads(BlockRead)

    context = {
        "request": request,
        "blocks": blocks,
    }

    if hx_request:
        return templates.TemplateResponse("components/block.html", context)

    return templates.TemplateResponse("base.html", context)


@router.get("/new", response_class=HTMLResponse)
async def new(request: Request):
    """
    Route to view new Block form.
    """
    context = {
        "request": request,
    }

    return templates.TemplateResponse("views/block-form.html", context)


@router.get("/edit/{id}", response_class=HTMLResponse)
async def edit(request: Request, id: str, hx_request: Optional[str] = Header(None)):
    """
    Route to edit and existing Block.
    """

    block_node = await db.read(id)

    context = {
        "request": request,
        "block_node": block_node,
    }

    if hx_request:
        return templates.TemplateResponse("views/block-edit-form.html", context)

    return templates.TemplateResponse("base.html", context)


@router.post("/create")
async def create_block(
    request: Request,
    name: str = Form(...),
    type: str = Form(...),
    model: str = Form(...),
    description: str = Form(...),
    tunnel_id: str = Form(...),
    hx_request: Optional[str] = Header(None),
):
    """
    Route to create a new Block Node in the database.
    """
    db = BlockOps()

    blocks = await db.create(
        BlockCreate(
            name=name,
            type=type,
            model=model,
            description=description,
            tunnel_id=tunnel_id,
        )
    )

    context = {
        "request": request,
        "blocks": blocks,
    }

    if hx_request:
        return templates.TemplateResponse("components/tunnel.html", context)

    return templates.TemplateResponse("base.html", context)


@router.get("/{id}")
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

    return templates.TemplateResponse("components/block.html", context)


# @router.delete("/blocks/delete")
# async def delete_blocks(request: Request):
#     """
#     Route to delete a All Blocks in the database.
#     """
#     db = BlockOps()

#     blocks = await db.deletes()

#     context = {
#         "request": request,
#         "blocks": blocks,
#     }

#     return templates.TemplateResponse("main.html", context)


# @router.delete("/blocks/delete/{id}")
# async def delete_block(request: Request, id: str):
#     """
#     Route to delete a Block by ID in the database.
#     """
#     db = BlockOps()

#     blocks = await db.delete(id)

#     context = {
#         "request": request,
#         "blocks": blocks,
#     }

#     return templates.TemplateResponse("main.html", context)
