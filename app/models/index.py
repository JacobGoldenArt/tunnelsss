from pydantic import BaseModel
from typing import List, Optional


class TunnelBase(BaseModel):
    child_blocks: Optional[List[str]] = []


class TunnelCreate(BaseModel):
    pass


class TunnelRead(BaseModel):
    id: str
    child_blocks: List[object] = None


class BlockBase(BaseModel):
    name: str
    type: str


class BlockCreate(BlockBase):
    pass


class BlockRead(BlockBase):
    id: str
