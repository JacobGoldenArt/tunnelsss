from typing import List
import uvicorn
from surrealdb import Surreal
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.models.index import TunnelCreate, TunnelRead, BlockCreate, BlockRead

api = FastAPI()

url = "ws://localhost:8000/rpc"
ns = "tunnels"
dbt = "tunnels"


@api.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


@api.get("/")
async def root():
    res = {"message": "Hello World"}
    return res


@api.post("/tunnels/create", response_model=TunnelRead)
async def create_tunnel(create: TunnelCreate):
    """
    Route to create a new Tunnel in the database.
    """
    async with Surreal(url) as db:
        await db.use(ns, dbt)
        make_tunnel: str = "tunnels:main"
        await db.create(make_tunnel, create)
        res = await db.select(make_tunnel)
        return res


@api.get("/tunnels/read", response_model=TunnelRead)
async def read_tunnel():
    """
    Route to read a Tunnel in the database.
    """
    async with Surreal(url) as db:
        await db.use(ns, dbt)
        res = await db.select("tunnels:main")
        return res


@api.delete("/tunnels/delete")
async def delete_tunnel():
    """
    Route to delete a Tunnel in the database.
    """
    async with Surreal(url) as db:
        await db.use(ns, dbt)
        await db.delete("tunnels")
        res = await db.select("tunnels:main")
        return res


@api.post("/blocks/create", response_model=List[BlockRead])
async def create_block(create: BlockCreate):
    """
    Route to create a new Tunnel in the database.
    """
    async with Surreal(url) as db:
        await db.use(ns, dbt)
        # await db.let("myblock", create)
        await db.query(
            """
            LET $myID = rand::uuid();
            CREATE blocks SET name = $myblock.name, type = $myblock.type, id = $myID;
    
            UPDATE tunnels:main SET child_blocks = [RETURN (SELECT * from blocks)]
            """,
            {"myblock": create},
        )
        res = await db.select("blocks")
        return res


@api.get("/blocks/read", response_model=List[BlockRead])
async def read_blocks():
    """
    Route to read a Tunnel in the database.
    """
    async with Surreal(url) as db:
        await db.use(ns, dbt)
        res = await db.select("blocks")
        return res


@api.get("/block/read/{id}", response_model=BlockRead)
async def read_block(id: str):
    """
    Route to read a Tunnel in the database.
    """
    async with Surreal(url) as db:
        await db.use(ns, dbt)
        res = await db.query(
            """
            RETURN SELECT blocks:$id from blocks
        """,
            {"id": id},
        )
        return res


@api.delete("/blocks/delete")
async def delete_blocks():
    """
    Route to delete a Tunnel in the database.
    """
    async with Surreal(url) as db:
        await db.use(ns, dbt)
        await db.delete("blocks")
        await db.query(
            """
            UPDATE tunnels:main SET child_blocks = [RETURN (SELECT * from blocks)]
        """
        )
        res = await db.select("blocks")
        return res


@api.delete("/blocks/delete/{id}", response_model=List[BlockRead])
async def delete_block(id: str):
    """
    Route to delete a Tunnel in the database.
    """
    async with Surreal(url) as db:
        await db.use(ns, dbt)
        await db.query(
            """
            RETURN DELETE $id; 
        """,
            {"id": id},
        )
        await db.query(
            """
            UPDATE tunnels:main SET child_blocks = [RETURN (SELECT * from blocks)]
        """
        )
        res = await db.select("blocks")
        return res


if __name__ == "__main__":
    uvicorn.run(api, host="localhost", port=8080, log_level="info")
