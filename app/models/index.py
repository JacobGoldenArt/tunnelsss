from pydantic import BaseModel
from typing import List, Optional


class TunnelBase(BaseModel):
    child_blocks: Optional[List[str]] = []


class TunnelCreate(TunnelBase):
    pass


class TunnelRead(BaseModel):
    id: str
    child_blocks: List[object] = None


class TunnelDelete(BaseModel):
    id: str


class BlockCreate(BaseModel):
    name: str
    type: str


class BlockRead(BaseModel):
    id: str
    name: Optional[str] = None
    type: Optional[str] = None


class BlockDelete(BaseModel):
    id: str
