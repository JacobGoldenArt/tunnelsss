from pydantic import BaseModel
from typing import List, Optional


class TunnelBase(BaseModel):
    child_blocks: Optional[List[str]] = []


class TunnelCreate(TunnelBase):
    name: str
    description: str


class TunnelRead(BaseModel):
    id: str
    name: str = None
    description: str = None
    child_blocks: List[object] = None


class TunnelDelete(BaseModel):
    id: str


class BlockCreate(BaseModel):
    name: str
    type: str
    model: str
    description: str
    tunnel_id: str


class BlockRead(BaseModel):
    id: str
    name: Optional[str] = None
    type: Optional[str] = None
    model: Optional[str] = None
    description: Optional[str] = None
    tunnel_id: str


class BlockDelete(BaseModel):
    id: str
