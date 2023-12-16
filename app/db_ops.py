from typing import List, Dict, Any
from app.models.index import TunnelRead, TunnelCreate, BlockRead, BlockCreate
from surrealdb import Surreal
from dataclasses import dataclass


db_config = {
    "url": "ws://localhost:8000/rpc",
    "ns": "tunnels",
    "dbt": "tunnels",
}


@dataclass
class TunnelOps:
    db_url: str = db_config["url"]
    db_ns: str = db_config["ns"]
    db_dbt: str = db_config["dbt"]

    @classmethod
    async def create(cls, create: TunnelCreate):
        """
        Route to create a new Tunnel in the database.
        """
        async with Surreal(cls.db_url) as db:
            await db.use(cls.db_ns, cls.db_dbt)

            await db.query(
                """
                LET $myID = rand::uuid();
                CREATE tunnels SET name = $my_tunnel.name, 
                description = $my_tunnel.description,
                child_blocks = [],
                id = $myID;
                """,
                {"my_tunnel": create},
            )

            results = await db.select("tunnels")
            return results

    @classmethod
    async def reads(cls, read: TunnelRead):
        """
        Route to read all Tunnel in the database.
        """
        async with Surreal(cls.db_url) as db:
            await db.use(cls.db_ns, cls.db_dbt)
            results = await db.select("tunnels")
            return results

    @classmethod
    async def read(cls, id: str):
        """
        Route to read a Tunnel in the database.
        """
        async with Surreal(cls.db_url) as db:
            await db.use(cls.db_ns, cls.db_dbt)
            results = await db.query(
                """
                SELECT * FROM $id;
            """,
                {"id": id},
            )
            return results

    @classmethod
    async def delete(cls):
        """
        Route to delete a Tunnel in the database.
        """
        async with Surreal(cls.db_url) as db:
            await db.use(cls.db_ns, cls.db_dbt)
            await db.delete("tunnels")
            results = await db.select("tunnels:main")
            return results


@dataclass
class BlockOps:
    db_url: str = db_config["url"]
    db_ns: str = db_config["ns"]
    db_dbt: str = db_config["dbt"]

    @classmethod
    async def create(cls, create: BlockCreate):
        """
        Route to create a new Tunnel in the database.
        """
        async with Surreal(cls.db_url) as db:
            await db.use(cls.db_ns, cls.db_dbt)
            # await db.let("myblock", create)
            await db.query(
                """
                LET $myID = rand::uuid();
                CREATE blocks SET name = $myblock.name, 
                type = $myblock.type, 
                description = $myblock.description,
                id = $myID,
                tunnel_id = $myblock.tunnel_id;
        
                UPDATE $myblock.tunnel_id SET child_blocks = [RETURN (SELECT * from blocks)]
                """,
                {"myblock": create},
            )
            results = await db.select("blocks")
            return results

    @classmethod
    async def reads(cls, read: BlockRead):
        """
        Route to read a Tunnel in the database.
        """
        async with Surreal(cls.db_url) as db:
            await db.use(cls.db_ns, cls.db_dbt)
            results = await db.select("blocks")
            return results

    @classmethod
    async def read(cls, id: str):
        """
        Route to read a Tunnel in the database.
        """
        async with Surreal(cls.db_url) as db:
            await db.use(cls.db_ns, cls.db_dbt)
            results = await db.query(
                """
                SELECT name,type,description FROM $id;
            """,
                {"id": id},
            )
            return results

    @classmethod
    async def deletes(cls):
        """
        Route to delete a Tunnel in the database.
        """
        async with Surreal(cls.db_url) as db:
            await db.use(cls.db_ns, cls.db_dbt)
            await db.delete("blocks")
            await db.query(
                """
                UPDATE tunnels:main SET child_blocks = [RETURN (SELECT * from blocks)]
            """
            )
            results = await db.select("blocks")
            return results

    @classmethod
    async def delete(cls, id: str):
        """
        Route to delete a Tunnel in the database.
        """
        async with Surreal(cls.db_url) as db:
            await db.use(cls.db_ns, cls.db_dbt)
            await db.query(
                """
                DELETE $id;
            """,
                {"id": id},
            )
            await db.query(
                """
                UPDATE tunnels:main SET child_blocks = [RETURN (SELECT * from blocks)]
            """
            )
            results = await db.select("blocks")
            return results
