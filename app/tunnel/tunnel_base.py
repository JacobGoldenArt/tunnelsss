from dataclasses import field
import asyncio
from typing import Dict, Any
from app.models.base_model import TunnelBase
from blocks.block_base import Block
from loguru import logger


class Tunnel(TunnelBase):
    """
    Represents a tunnel of blocks.
    """

    def add_block(self, block: Block) -> None:
        """
        Add a block to the tunnel.
        """

    def connect_blocks(self, source_block_name: str, target_block_name: str) -> None:
        """
        Connect two blocks in the tunnel.
        """

    async def run(self, data: Any) -> None:
        """
        Run the tunnel with the given data.
        """
        await asyncio.gather(data)
